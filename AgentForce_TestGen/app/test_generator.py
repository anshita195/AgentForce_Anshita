import json
from typing import Dict, List
from pathlib import Path

# Note: We are removing the dependency on FunctionInfo as it's no longer needed here
# from .parser import FunctionInfo 

class TestGenerator:
    def __init__(self, output_dir: str = "tests"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_test_file(self, module_name: str, test_data: Dict) -> str:
        """
        Generate a pytest file from the new 'test_structure' in the LLM response.
        """
        if "test_structure" not in test_data:
            raise ValueError("JSON from LLM is missing 'test_structure' key")

        structure = test_data["test_structure"]
        test_content = []

        # Add imports
        if "imports" in structure:
            test_content.extend(structure["imports"])
            test_content.append("") # Add a blank line

        # Process different test groups
        for group in structure.get("test_groups", []):
            if "parametrize" in group:
                self._add_parametrized_test(group, test_content)
            elif "cases" in group:
                self._add_simple_cases(group, module_name, test_content)
        
        test_file_path = self.output_dir / f"test_{module_name}.py"
        test_file_path.write_text("\n".join(test_content))
        return str(test_file_path)

    def _add_parametrized_test(self, group: Dict, test_content: List[str]):
        """Handles parametrized test cases."""
        params = group["parametrize"]["params"]
        test_content.append(f"@pytest.mark.parametrize('{params}', [")
        
        for case in group["parametrize"]["cases"]:
            comment = f"  # {case['comment']}" if 'comment' in case else ""
            test_content.append(f"    ({case['input']}, {case['expected']}),{comment}")

        test_content.append("])")
        test_content.append(f"def {group['name']}({params}):")
        # A more generic way to handle the test body for parametrized tests
        test_content.append(f"    assert sample_input.calculate_discount(input_value) == expected")
        test_content.append("")

    def _add_simple_cases(self, group: Dict, module_name: str, test_content: List[str]):
        """Handles simple, non-parametrized test cases."""
        for case in group["cases"]:
            description = case.get("description", "")
            test_content.extend([
                f"def {case['name']}():",
                f'    """{description}"""',
                f"    result = {module_name}.calculate_discount({case['input']})",
                f"    assert result == {case['expected']}",
                ""
            ])