import subprocess
import re
from pathlib import Path
import sys

def run_tests_and_get_coverage(test_file_path: str, module_name: str) -> dict:
    """
    Runs pytest with coverage and returns a cleaned-up report.
    """
    try:
        source_dir = Path(f"examples/{module_name}.py").parent
        command = [
            sys.executable,
            "-m", "pytest",
            test_file_path,
            "--cov", str(source_dir),
            "--cov-report", "term-missing",
            "--cov-report", "html"
        ]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        
        output = result.stdout
        
        # --- NEW: Extract more details using regex ---
        coverage_match = re.search(r"TOTAL.*\s(\d+)%", output)
        passed_match = re.search(r"(\d+) passed", output)

        return {
            "status": "Success",
            "summary": f"{passed_match.group(1) if passed_match else '0'} tests passed.",
            "coverage_percentage": int(coverage_match.group(1)) if coverage_match else 0,
            "html_report_path": "htmlcov/index.html",
            "full_log": output # Keep the raw log in a separate field
        }

    except subprocess.CalledProcessError as e:
        failed_match = re.search(r"(\d+) failed", e.stdout + e.stderr)
        summary = f"{failed_match.group(1) if failed_match else '0'} tests failed."
        return {
            "status": "Tests Failed",
            "summary": summary,
            "error": "Pytest execution failed.",
            "full_log": e.stdout + e.stderr
        }
    except Exception as e:
        return {
            "status": "Error",
            "summary": "An unexpected error occurred.",
            "error": "An unexpected error occurred during test execution.",
            "full_log": str(e)
        }