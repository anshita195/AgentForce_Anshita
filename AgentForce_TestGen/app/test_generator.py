import json
from typing import Dict, List, Union
from pathlib import Path

class TestGenerator:
    def __init__(self, output_dir: str = "tests"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_test_file(self, module_name: str, test_data: Union[str, Dict]) -> str:
        """Generate a pytest file from the LLM response"""
        if isinstance(test_data, str):
            test_data = json.loads(test_data)

        test_content = []
        
        # Add imports
        test_content.extend(test_data["test_structure"]["imports"])
        test_content.extend(["", ""])

        # Process each test group
        for group in test_data["test_structure"]["test_groups"]:
            if group.get("parametrize"):
                # Generate parametrized test
                cases = [
                    f"    ({case['input']}, {case['expected']})  # {case['comment']}"
                    for case in group["parametrize"]["cases"]
                ]
                
                test_content.extend([
                    f"@pytest.mark.parametrize('{group['parametrize']['params']}', [",
                    ",\n".join(cases),
                    "])",
                    f"def {group['name']}(input_value, expected):",
                    f"    '''Test various input scenarios'''",
                    f"    result = sample_input.calculate_discount(input_value)",
                    "    assert result == expected",
                    "",
                    ""
                ])
            elif group.get("is_slow"):
                # Generate performance test
                test_content.extend([
                    "@pytest.mark.slow",
                    f"def {group['name']}():",
                    f"    '''{group['description']}'''",
                    f"    large_input = [(1.0, 1)] * {group['input_size']}",
                    f"    result = sample_input.calculate_discount(large_input)",
                    f"    assert result == pytest.approx({group['input_size']} * 0.1)",
                    "",
                    ""
                ])
            else:
                # Generate individual test cases
                for case in group["cases"]:
                    test_content.extend([
                        f"def {case['name']}():",
                        f"    '''{case['description']}'''",
                        f"    result = sample_input.calculate_discount({case['input']})",
                        f"    assert result == {case['expected']}",
                        "",
                        ""
                    ])

        test_file = self.output_dir / f"test_{module_name}.py"
        test_file.write_text("\n".join(test_content))
        return str(test_file)