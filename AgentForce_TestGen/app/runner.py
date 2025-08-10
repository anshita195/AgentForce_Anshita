import subprocess
import re
from pathlib import Path
import sys

def run_tests_and_get_coverage(test_file_path: str, module_name: str) -> dict:
    """
    Runs pytest and returns a cleaned-up report.
    (Temporarily disabled coverage to fix a subprocess bug).
    """
    try:
        # --- MODIFIED: The command now runs pytest without coverage ---
        command = [
            sys.executable,
            "-m", "pytest",
            test_file_path
        ]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        
        output = result.stdout
        
        passed_match = re.search(r"(\d+)\s+passed", output)
        summary = f"{passed_match.group(1) if passed_match else '0'} tests passed."

        return {
            "status": "Success",
            "summary": summary,
            "coverage_percentage": "Coverage reporting is temporarily disabled to resolve a bug.",
            "full_log": output
        }

    except subprocess.CalledProcessError as e:
        stdout = e.stdout or ""
        stderr = e.stderr or ""
        return {
            "status": "Tests Failed",
            "summary": "Pytest execution failed.",
            "error": "Pytest process returned a non-zero exit code.",
            "full_log": stdout + stderr
        }
    except Exception as e:
        return {
            "status": "Error",
            "summary": "An unexpected error occurred during test execution.",
            "error": str(e)
        }