from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import json
from pathlib import Path
from typing import Dict, Any

# --- Python Tools ---
from .parser import CodeParser  # <-- THIS LINE WAS MISSING
from .llm import LLMWrapper
from .test_generator import TestGenerator
from .runner import run_tests_and_get_coverage

# --- JavaScript Tools ---
from .js_parser import parse_js_file
from .js_test_generator import JSTestGenerator
from .js_runner import run_js_tests_and_get_coverage

# --- Compatibility Function ---
def map_test_cases_to_new_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    If the old 'test_cases' format is detected, map it to the new schema.
    """
    if "test_cases" in data and "tests" not in data:
        describes = {}
        for case in data["test_cases"]:
            func_name = case["function"]
            if func_name not in describes:
                describes[func_name] = {
                    "describe": func_name,
                    "cases": []
                }
            describes[func_name]["cases"].append({
                "it": f"should handle input {case['input']}",
                "function_to_test": func_name,
                "input": str(case['input']),
                "expected_output": case['expected_output']
            })
        
        func_names = ", ".join(describes.keys())

        return {
            "imports": f"const {{ {func_names} }} = require('../examples/sample_input');",
            "tests": list(describes.values())
        }
    return data

app = FastAPI(
    title="TestGen",
    description="AI-powered test case generator for multiple languages",
    version="0.3.2" # Version bump!
)

# --- Tool Instances ---
py_parser = CodeParser()
llm = LLMWrapper()
py_test_gen = TestGenerator()
js_test_gen = JSTestGenerator()

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
        test_data_str = llm.generate_tests(content_str, functions)
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
            js_functions = parse_js_file(content_str)
            test_data_str = llm.generate_js_tests(content_str, js_functions)
            raw_json = json.loads(test_data_str)
            test_json = map_test_cases_to_new_schema(raw_json)
            module_name = Path(file.filename).stem
            test_file_path = js_test_gen.generate_test_file(module_name, test_json)
            coverage_results = run_js_tests_and_get_coverage(test_file_path, module_name)
            return {
                "language": "javascript",
                "message": "JavaScript tests generated and executed successfully",
                "test_file_path": test_file_path,
                "coverage_report": coverage_results
            }
        except (RuntimeError, ValueError, FileNotFoundError) as e:
            raise HTTPException(500, f"Error processing JavaScript file: {str(e)}")

    else:
        raise HTTPException(400, "Unsupported language. Please choose 'python' or 'javascript'.")