import os
import google.generativeai as genai
from typing import Dict, List, Any
from dotenv import load_dotenv
from pathlib import Path
import json
from .parser import FunctionInfo # Keep for Python

class LLMWrapper:
    def __init__(self):
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            print("Successfully initialized Gemini model")
        except Exception as e:
            print(f"Error initializing Gemini: {str(e)}")
            raise

    def _generate_content(self, prompt: str) -> str:
        # (This helper function remains the same as before)
        try:
            generation_config = {"temperature": 0.7, "top_k": 1, "max_output_tokens": 2048}
            response = self.model.generate_content(
                contents=[{"parts": [{"text": prompt}]}],
                generation_config=generation_config
            )
            result = response.text.strip()
            try:
                json.loads(result)
                return result
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'({[\s\S]*})', result)
                if json_match:
                    return json_match.group(1)
                raise ValueError("Could not extract valid JSON from response")
        except Exception as e:
            print(f"Error generating tests: {str(e)}")
            raise

    # --- PYTHON TEST GENERATION (remains the same) ---
    def generate_tests(self, code: str, functions: List[FunctionInfo]) -> str:
        prompt = self._build_py_prompt(code, functions)
        return self._generate_content(prompt)

    def _build_py_prompt(self, code: str, functions: List[FunctionInfo]) -> str:
        # (This function remains the same as before)
        function_info_str = "\n".join(
            f"- {f.name}({', '.join(f.args)}): {f.docstring or 'No docstring'}"
            for f in functions
        )
        return f"""You are a test generation assistant. Generate pytest unit tests for the following Python code.
Your response must be valid JSON in exactly this format, with no additional text:
{{
  "test_structure": {{ ... }}
}}
Here is the code to test:
{code}
Function information:
{function_info_str}
Remember: Return ONLY valid JSON, no other text or formatting."""

    # --- REVISED JAVASCRIPT TEST GENERATION ---
    def generate_js_tests(self, code: str, functions: List[Dict]) -> str:
        prompt = self._build_js_prompt(code, functions)
        return self._generate_content(prompt)

    def _build_js_prompt(self, code: str, functions: List[Dict]) -> str:
        function_info_str = "\n".join(
            f"- {f['name']}({', '.join(f['args'])})"
            for f in functions
        )
        return f"""You are a test generation assistant. Generate Jest unit tests for the following JavaScript code.
Your response must be valid JSON in exactly this format, with no additional text:

{{
  "imports": "const {{ <function1>, <function2> }} = require('../examples/<filename>');",
  "tests": [
    {{
      "describe": "<describe_block_for_a_function>",
      "cases": [
        {{
          "it": "<it_block_description>",
          "function_to_test": "<name_of_function_being_tested>",
          "input": "<test_input>",
          "expected": "<full_jest_matcher_string, e.g., toBe(5) or toEqual([1,2])>"
        }}
      ]
    }}
  ]
}}

Here is the code to test:
{code}

Function information:
{function_info_str}

IMPORTANT: For each test case in the 'cases' array, you MUST include the 'function_to_test' key with the name of the function that should be called.

Remember: Return ONLY valid JSON, no other text or formatting."""