from pathlib import Path
from typing import Dict, List
import re

class JSTestGenerator:
    def __init__(self, output_dir: str = "js_tests"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_test_file(self, module_name: str, test_data: Dict) -> str:
        """
        Generate a Jest test file from the LLM's JSON response,
        with added logic to fix common AI mistakes.
        """
        if not all(k in test_data for k in ["imports", "tests"]):
            raise ValueError("JSON from LLM is missing 'imports' or 'tests' keys.")

        test_content = []

        # --- FIX 1: Take control of the module path ---
        # The LLM will provide the function names, but we'll build the path.
        try:
            # Extracts function names like 'calculateFactorial, greet' from the string
            function_names = re.search(r'\{\s*(.*?)\s*\}', test_data["imports"]).group(1)
            imports_line = f"const {{ {function_names} }} = require('../examples/{module_name}');"
        except (AttributeError, IndexError):
            # Fallback if the regex fails
            imports_line = f"// Could not parse imports, please check manually."

        test_content.append(imports_line)
        test_content.append("")

        for test_suite in test_data.get("tests", []):
            describe_name = test_suite.get("describe", "Test Suite")
            test_content.append(f"describe('{describe_name}', () => {{")

            for case in test_suite.get("cases", []):
                required_keys = ["it", "function_to_test", "input", "expected"]
                if not all(k in case for k in required_keys):
                    continue

                it_desc = case["it"]
                func_name = case["function_to_test"]
                input_val = case["input"]
                expected_val = case["expected"]
                
                # --- FIX 2: Correct unquoted string inputs ---
                # If the input is for the 'greet' function and isn't a number, wrap it in quotes.
                if func_name == 'greet' and not input_val.replace('.', '', 1).isdigit():
                     if not (input_val.startswith("'") or input_val.startswith('"')):
                         input_val = f"'{input_val}'"


                test_content.extend([
                    f"  it('{it_desc}', () => {{",
                    f"    expect({func_name}({input_val})).{expected_val};",
                    "  });"
                ])
            
            test_content.append("});")
            test_content.append("")

        test_file_path = self.output_dir / f"{module_name}.test.js"
        test_file_path.write_text("\n".join(test_content))
        return str(test_file_path)