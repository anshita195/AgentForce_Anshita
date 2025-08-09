from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import json
from pathlib import Path
from .parser import CodeParser
from .llm import LLMWrapper
from .test_generator import TestGenerator
from .runner import run_tests_and_get_coverage

app = FastAPI(
    title="TestGen",
    description="AI-powered test case generator for Python code",
    version="0.1.0"
)

parser = CodeParser()
llm = LLMWrapper()
test_gen = TestGenerator()

@app.post("/generate")
async def generate_tests(file: UploadFile = File(...)):
    """Generate test cases from uploaded Python file"""
    if not file.filename.endswith('.py'):
        raise HTTPException(400, "Only Python files are supported")
    
    try:
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Parse the code
        functions = parser.parse_file(content_str)
        
        # Generate tests using LLM
        test_data_str = llm.generate_tests(content_str, functions)
        
        # Convert string response to JSON
        try:
            test_json = json.loads(test_data_str)
        except json.JSONDecodeError:
            raise HTTPException(500, f"Invalid JSON response from LLM: {test_data_str}")

        # --- MODIFIED: No longer checking for 'functions' key ---
        # The new test_generator will handle the validation internally
        
        # Generate test file
        module_name = Path(file.filename).stem
        # The updated generator now correctly handles the 'test_structure' format
        test_file_path = test_gen.generate_test_file(module_name, test_json)
        
        # Run tests and get coverage
        coverage_results = run_tests_and_get_coverage(test_file_path, module_name)
        
        # --- MODIFIED: Simplified the response for now ---
        return {
            "message": "Tests generated and executed successfully",
            "test_file_path": test_file_path,
            "functions_analyzed": len(functions),
            # We can add a more sophisticated test count later
            "coverage_report": coverage_results
        }
    except Exception as e:
        raise HTTPException(500, f"An error occurred: {str(e)}")

         
        