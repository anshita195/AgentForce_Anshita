from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import json
from pathlib import Path
from .parser import CodeParser
from .llm import LLMWrapper
from .test_generator import TestGenerator

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
        if not functions:
            raise HTTPException(400, "No testable functions found in file")
        
        # Generate tests using LLM (returns JSON string)
        test_json = llm.generate_tests(content_str, functions)
        
        # Generate test file from JSON string
        module_name = Path(file.filename).stem
        test_file = test_gen.generate_test_file(module_name, test_json)
        
        return {
            "message": "Tests generated successfully",
            "test_file": test_file,
            "functions_analyzed": len(functions)
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error processing file: {str(e)}")



# @app.post("/generate")
# async def generate_tests(file: UploadFile = File(...)):
#     """Generate test cases from uploaded Python file"""
#     if not file.filename.endswith('.py'):
#         raise HTTPException(400, "Only Python files are supported")
    
#     content = await file.read()
#     content_str = content.decode('utf-8')
    
#     # Parse the code
#     functions = parser.parse_file(content_str)
    
#     # Generate tests using LLM
#     test_data = llm.generate_tests(content_str, functions)
    
#     # Convert string response to JSON
#     try:
#         test_json = json.loads(test_data)
#     except json.JSONDecodeError:
#         raise HTTPException(500, "Invalid JSON response from LLM")
    
#     # Generate test file
#     module_name = Path(file.filename).stem
#     test_file = test_gen.generate_test_file(module_name, test_json)
    
#     return {
#         "message": "Tests generated successfully",
#         "test_file": test_file,
#         "functions_analyzed": len(functions),
#         "tests_generated": sum(len(f["tests"]) for f in test_json["functions"])
#     }

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)