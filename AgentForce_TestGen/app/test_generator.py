import json
from typing import Dict, List
from pathlib import Path
from .parser import FunctionInfo

class TestGenerator:
    def __init__(self, output_dir: str = "tests"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_test_file(self, module_name: str, test_data: Dict) -> str:
        """Generate a pytest file from the LLM response"""
        test_content = [
            "import pytest",
            f"import {module_name}",
            ""
        ]

        for func in test_data["functions"]:
            for test in func["tests"]:
                test_content.extend([
                    f"def {test['test_name']}():",
                    f'    """{test["type"]}: {test.get("description", "")}\n"""',
                    f"    result = {module_name}.{func['name']}({test['input']})",
                    f"    assert result == {test['expected']}",
                    ""
                ])

        test_file = self.output_dir / f"test_{module_name}.py"
        test_file.write_text("\n".join(test_content))
        return str(test_file)