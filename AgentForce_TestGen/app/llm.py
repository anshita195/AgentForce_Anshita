import os
import google.generativeai as genai
from typing import Dict, List, Any
from dotenv import load_dotenv
from pathlib import Path
import json
from .parser import FunctionInfo

class LLMWrapper:
    def __init__(self):
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        try:
            # Use the specific flash model version
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            print("Successfully initialized Gemini model")
        except Exception as e:
            print(f"Error initializing Gemini: {str(e)}")
            raise

    def generate_tests(self, code: str, functions: List[FunctionInfo]) -> str:
        try:
            prompt = self._build_prompt(code, functions)
            
            # Configure generation parameters for flash model
            generation_config = {
                "temperature": 0.7,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
            
            # Generate response
            response = self.model.generate_content(
                contents=[{
                    "parts": [{"text": prompt}]
                }],
                generation_config=generation_config
            )
            
            # Validate JSON response
            result = response.text.strip()
            try:
                # Verify it's valid JSON
                json.loads(result)
                return result
            except json.JSONDecodeError:
                # If not valid JSON, try to extract JSON portion
                import re
                json_match = re.search(r'({[\s\S]*})', result)
                if json_match:
                    return json_match.group(1)
                raise ValueError("Could not extract valid JSON from response")
                
        except Exception as e:
            print(f"Error generating tests: {str(e)}")
            raise

    def _build_prompt(self, code: str, functions: List[FunctionInfo]) -> str:
        return f"""You are a test generation assistant. Generate pytest unit tests for the following Python code.
Your response must be valid JSON in exactly this format, with no additional text:

{{
  "language": "python",
  "functions": [
    {{
      "name": "<function_name>",
      "tests": [
        {{
          "test_name": "<test_name>",
          "type": "unit",
          "input": "<test_input>",
          "expected": "<expected_output>"
        }}
      ],
      "edge_cases": ["<edge_case1>", "<edge_case2>"],
      "performance_warnings": "<warning_text>"
    }}
  ]
}}

Here is the code to test:

{code}

Function information:
{self._format_functions(functions)}

Remember: Return ONLY valid JSON, no other text or formatting."""

    def _format_functions(self, functions: List[FunctionInfo]) -> str:
        return "\n".join(
            f"- {f.name}({', '.join(f.args)}): {f.docstring or 'No docstring'}"
            for f in functions
        )