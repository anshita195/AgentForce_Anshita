import os
import json
import google.generativeai as genai
from typing import Dict, List
from dotenv import load_dotenv
from pathlib import Path
from .parser import FunctionInfo

class LLMWrapper:
    def __init__(self):
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_tests(self, code: str, functions: List[FunctionInfo]) -> str:
      """Generate tests and return as JSON string"""
      try:
          prompt = self._build_prompt(code, functions)
          response = self.model.generate_content(prompt)
          
          # Extract JSON from response
          text = response.text.strip()
          
          # Try to find JSON in the response
          start_idx = text.find('{')
          end_idx = text.rfind('}')
          
          if start_idx != -1 and end_idx != -1:
              json_str = text[start_idx:end_idx + 1]
              # Validate JSON by parsing and re-stringifying
              json.loads(json_str)  # Will raise JSONDecodeError if invalid
              return json_str
          else:
              return json.dumps(self._generate_fallback_tests(functions[0].name))
              
      except Exception as e:
          print(f"Error generating tests: {str(e)}")
          return json.dumps(self._generate_fallback_tests(functions[0].name))
    def _generate_fallback_tests(self, func_name: str) -> Dict:
        """Generate basic test structure if LLM fails"""
        return {
            "test_structure": {
                "imports": [
                    "import pytest",
                    "from examples import sample_input"
                ],
                "test_groups": [
                    {
                        "name": "test_basic_scenarios",
                        "parametrize": {
                            "params": "input_value,expected",
                            "cases": [
                                {
                                    "input": "[]",
                                    "expected": "0.0",
                                    "comment": "empty list returns zero"
                                },
                                {
                                    "input": "[(50, 1)]",
                                    "expected": "0.0",
                                    "comment": "below threshold"
                                },
                                {
                                    "input": "[(60, 2)]",
                                    "expected": "pytest.approx(12.0)",
                                    "comment": "above threshold"
                                }
                            ]
                        }
                    },
                    {
                        "name": "test_boundary_cases",
                        "cases": [
                            {
                                "name": "test_exact_threshold",
                                "input": "[(50, 2)]",
                                "expected": "0.0",
                                "description": "total exactly 100 should give no discount"
                            }
                        ]
                    },
                    {
                        "name": "test_performance",
                        "is_slow": True,
                        "input_size": 100000,
                        "description": "Test with large cart"
                    }
                ]
            }
        }

    def _build_prompt(self, code: str, functions: List[FunctionInfo]) -> str:
        return f"""Act as an expert test engineer. Analyze this Python function and generate comprehensive pytest test cases.
    Follow these STRICT requirements:

    1. Code to analyze:
    {code}

    2. Function info:
    {self._format_functions(functions)}

    3. Test Requirements:
    - Use pytest.mark.parametrize for similar test cases
    - Use pytest.approx for ALL float comparisons
    - Include tests for:
    * Empty/None inputs
    * Boundary conditions (exactly at threshold)
    * Edge cases (malformed inputs)
    * Float precision cases
    * Performance tests (marked with @pytest.mark.slow)

    Return ONLY valid JSON in this exact format:
    {{
    "test_structure": {{
        "imports": [
        "import pytest",
        "from examples import sample_input"
        ],
        "test_groups": [
        {{
            "name": "test_basic_scenarios",
            "parametrize": {{
            "params": "input_value,expected",
            "cases": [
                {{"input": "[]", "expected": "0.0", "comment": "empty list"}},
                {{"input": "[(50, 1)]", "expected": "0.0", "comment": "below threshold"}},
                {{"input": "[(60, 2)]", "expected": "pytest.approx(12.0)", "comment": "above threshold"}}
            ]
            }}
        }},
        {{
            "name": "test_boundary_cases",
            "cases": [
            {{
                "name": "test_exact_threshold",
                "input": "[(50, 2)]",
                "expected": "0.0",
                "description": "total exactly 100 should give no discount"
            }}
            ]
        }},
        {{
            "name": "test_performance",
            "is_slow": true,
            "input_size": 100000,
            "description": "Test with large cart"
        }}
        ]
    }}
    }}

    Important requirements:
    1. ALL float comparisons MUST use pytest.approx
    2. Include boundary test for total == 100
    3. Test malformed inputs (should raise TypeError/ValueError)
    4. Test float precision cases
    5. Mark performance tests with @pytest.mark.slow"""