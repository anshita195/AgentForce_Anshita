import subprocess
import json
from pathlib import Path
from typing import Dict, Any

def run_js_tests_and_get_coverage(test_file_path: str, module_name: str) -> Dict[str, Any]:
    """
    Runs Jest with coverage and returns a parsed report.
    """
    try:
        project_root = Path(__file__).parent.parent
        jest_cli_path = project_root / "node_modules" / "jest" / "bin" / "jest.js"

        if not jest_cli_path.exists():
            raise FileNotFoundError("jest.js not found. Please run 'npm install jest'.")

        source_file = project_root / "examples" / f"{module_name}.js"
        results_path = project_root / 'jest_results.json'
        
        command = [
            "node",
            str(jest_cli_path),
            test_file_path,
            "--coverage",
            f"--collectCoverageFrom={source_file}",
            "--json",
            f"--outputFile={results_path}"
        ]

        # Execute the command from the project root
        subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8' # <-- THE CRUCIAL FIX
        )

        # Read the JSON output file created by Jest
        with open(results_path, 'r', encoding='utf-8') as f:
            results = json.load(f)

        # Clean up the results file
        if results_path.exists():
            results_path.unlink()

        summary = f"{results.get('numPassedTests', 0)} tests passed out of {results.get('numTotalTests', 0)}."
        coverage_pct = 0
        # Correctly resolve path for Windows/Linux
        source_file_key = str(source_file.resolve())
        if source_file_key in results.get("coverageMap", {}):
             coverage_pct = results["coverageMap"][source_file_key].get("statements", {}).get("pct", 0)

        return {
            "status": "Success" if results.get('numFailedTests', 0) == 0 else "Tests Failed",
            "summary": summary,
            "coverage_percentage": coverage_pct,
            "full_log": results
        }

    except subprocess.CalledProcessError as e:
        # Robustly handle stdout/stderr which might be None
        stdout = e.stdout or ""
        stderr = e.stderr or ""
        return {
            "status": "Error",
            "summary": "Jest execution failed.",
            "error": "Jest process returned a non-zero exit code.",
            "full_log": stdout + stderr
        }
    except Exception as e:
        return {
            "status": "Error",
            "summary": "An unexpected error occurred during test execution.",
            "error": str(e)
        }