import subprocess
import re
from pathlib import Path
import sys
from typing import Dict, Any

def run_js_tests_and_get_coverage(test_file_path: str, module_name: str) -> Dict[str, Any]:
    """
    Runs Jest with coverage and returns a parsed report.

    Args:
        test_file_path: The path to the generated Jest test file.
        module_name: The name of the original module that was tested.

    Returns:
        A dictionary containing the test status and coverage report.
    """
    try:
        # Path to the source file to measure coverage against
        source_file = Path("examples") / f"{module_name}.js"

        # The command to run Jest
        # We use 'npx jest' to ensure we're using the project's installed version
        command = [
            "npx", "jest",
            test_file_path,
            "--coverage", # Enable coverage collection
            f"--collectCoverageFrom={source_file}", # Specify which file to track
            "--json", # Output results in a machine-readable JSON format
            "--outputFile=jest_results.json" # Specify where to save the JSON output
        ]

        # Execute the command from the project root
        project_root = Path(__file__).parent.parent
        subprocess.run(
            command,
            cwd=project_root, # Run the command in the root directory
            capture_output=True,
            text=True,
            check=True
        )

        # Read the JSON output file created by Jest
        results_path = project_root / "jest_results.json"
        with open(results_path, 'r') as f:
            results = json.load(f)

        # Clean up the results file
        results_path.unlink()

        # Parse the results for our final report
        summary = f"{results.get('numPassedTests', 0)} tests passed out of {results.get('numTotalTests', 0)}."
        coverage_data = results.get("coverageMap", {}).get(str(source_file.resolve()), {})
        coverage_pct = coverage_data.get("statements", {}).get("pct", 0)

        return {
            "status": "Success" if results.get('numFailedTests', 0) == 0 else "Tests Failed",
            "summary": summary,
            "coverage_percentage": coverage_pct,
            "full_log": results # The full JSON log for debugging
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "Error",
            "summary": "Jest execution failed.",
            "error": e.stderr,
            "full_log": e.stdout + e.stderr
        }
    except Exception as e:
        return {
            "status": "Error",
            "summary": "An unexpected error occurred during test execution.",
            "error": str(e)
        }