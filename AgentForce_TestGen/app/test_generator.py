import json
from typing import Dict, List, Any
from pathlib import Path
import re

class TestGenerator:
    def __init__(self, output_dir: str = "tests"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def _format_py_value(self, value: Any) -> str:
        """Formats a Python value for inclusion in the test code."""
        if isinstance(value, str):
            # Escape single quotes within the string
            return f"'{value.replace("'", "\\'")}'"
        return str(value)

    def generate_test_file(self, module_name: str, test_data: Dict) -> str:
        """Generate a pytest file from the LLM response."""
        test_content = [
            "import pytest",
            f"from examples import {module_name}",
            ""
        ]

        test_counter = 1
        for group in test_data.get("test_groups", []):
            for case in group.get("cases", []):
                if "input" not in case or "expected_output" not in case:
                    continue

                input_val = case["input"]
                expected_out = case["expected_output"]

                # --- FIX: Use a simple and safe counter for test names ---
                test_name = f"test_{module_name}_{test_counter}"
                test_counter += 1

                test_content.extend([
                    f"def {test_name}():",
                    f"    # Test with input: {input_val}",
                    f"    result = {module_name}.calculate_discount({input_val})"
                ])

                if isinstance(expected_out, float):
                    test_content.append(f"    assert result == pytest.approx({expected_out})")
                else:
                    formatted_expected = self._format_py_value(expected_out)
                    test_content.append(f"    assert result == {formatted_expected}")

                test_content.append("")

        test_file = self.output_dir / f"test_{module_name}.py"
        test_file.write_text("\n".join(test_content))
        return str(test_file)