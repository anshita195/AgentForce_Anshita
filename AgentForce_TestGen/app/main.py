from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import json
from pathlib import Path

# --- Python Tools ---
from .parser import CodeParser
from .llm import LLMWrapper
from .test_generator import TestGenerator
from .runner import run_tests_and_get_coverage

# --- JavaScript Tools ---
from .js_parser import parse_js_file
from .js_test_generator import JSTestGenerator # <-- NEW: Import the JS test generator


app = FastAPI(
    title="TestGen",
    description="AI-powered test case generator for multiple languages",
    version="0.2.0"
)

# --- Tool Instances ---
py_parser = CodeParser()
llm = LLMWrapper() # The same LLM wrapper can be used for both
py_test_gen = TestGenerator()
js_test_gen = JSTestGenerator() # <-- NEW: Create an instance for the JS generator


@app.post("/generate")
async def generate_tests(
    language: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Generate test cases for an uploaded file in the specified language.
    """
    if language == "python":
        if not file.filename.endswith('.py'):
            raise HTTPException(400, "For Python, only .py files are supported")

        content_str = (await file.read()).decode('utf-8')

        functions = py_parser.parse_file(content_str)
        test_data_str = llm.generate_tests(content_str, functions) # This is the python-specific method
        test_json = json.loads(test_data_str)

        module_name = Path(file.filename).stem
        test_file_path = py_test_gen.generate_test_file(module_name, test_json)

        coverage_results = run_tests_and_get_coverage(test_file_path, module_name)

        return {
            "language": "python",
            "message": "Python tests generated and executed successfully",
            "test_file_path": test_file_path,
            "coverage_report": coverage_results
        }

    elif language == "javascript":
        if not file.filename.endswith('.js'):
            raise HTTPException(400, "For JavaScript, only .js files are supported")

        content_str = (await file.read()).decode('utf-8')

        try:
            # Step 1: Parse the JS file
            js_functions = parse_js_file(content_str)

            # Step 2: Generate the test plan using the LLM
            test_data_str = llm.generate_js_tests(content_str, js_functions)
            test_json = json.loads(test_data_str)

            # Step 3: Generate the actual .test.js file
            module_name = Path(file.filename).stem
            test_file_path = js_test_gen.generate_test_file(module_name, test_json)

            # We will add the JS test runner in the next major step.
            # For now, confirm the file was created.
            return {
                "language": "javascript",
                "message": "JavaScript test file generated successfully!",
                "test_file_path": test_file_path,
                "note": "JavaScript test execution and coverage reporting will be added next."
            }
        except (RuntimeError, ValueError) as e:
            raise HTTPException(500, f"Error processing JavaScript file: {str(e)}")

    else:
        raise HTTPException(400, "Unsupported language. Please choose 'python' or 'javascript'.")