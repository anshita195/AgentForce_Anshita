TestGen AI Agent
TestGen is an intelligent developer agent designed to automate the creation of unit tests. It analyzes Python and JavaScript code, understands its logic and flow, and generates meaningful test cases, complete with execution results and code coverage reports.

This project was developed to address the "Track 2: Developer Agents - Problem 1: Test Case Generator Bot" challenge.

✨ Features
Multi-Language Support: Seamlessly generates tests for both Python and JavaScript code.

Intelligent Test Case Generation: Goes beyond simple boilerplate by creating tests that cover different logical paths and edge conditions (e.g., empty inputs, zero values, negative numbers).

Automated Test Execution: The agent doesn't just write tests; it runs them using the appropriate frameworks (pytest for Python, Jest for JavaScript).

Comprehensive Coverage Reports: Delivers a precise, quantifiable code coverage percentage with every run, providing immediate insight into test quality.

Robust API: Built with FastAPI, providing a clean, simple, and effective endpoint for code submission.

Resilient AI Interaction: Implements a retry mechanism and schema validation (jsonschema) to ensure the AI's output is always structured and reliable.

🤖 Agent Architecture: How It Works
TestGen operates on a sophisticated four-step pipeline to interpret code and produce high-quality tests.

1. Parse & Understand
When a code file is submitted, the agent first uses an Abstract Syntax Tree (AST) to parse the code. This initial step identifies the core components, such as function names and arguments.

Python: Uses Python's built-in ast module.

JavaScript: Uses the acorn library via a Node.js subprocess.

2. Plan & Reason
The structured information from the AST is sent to a Generative AI (Google's Gemini model). The AI is given a carefully engineered prompt that instructs it to act as an "expert test engineer." It analyzes the function signatures and code logic to reason about potential inputs, expected outputs, and edge cases. Its plan is returned as a structured JSON object.

3. Generate
The validated JSON plan from the AI is passed to a dedicated Test Generator module. This component translates the AI's abstract plan into a concrete, syntactically correct test file using the appropriate testing framework (pytest or Jest).

4. Execute & Report
Finally, the agent's Runner module executes the newly generated test file in a secure subprocess. It captures the results and, most importantly, the code coverage report. This complete analysis is then sent back to the user in the API response.

🚀 Getting Started
Prerequisites
Python 3.10+

Node.js 14+ and npm

A Google Gemini API Key

1. Clone the Repository
git clone <your-repository-url>
cd AgentForce_TestGen

2. Set Up Environment Variables
Create a file named .env in the project root and add your Gemini API key:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

3. Install Dependencies
Python Dependencies:

pip install -r requirements.txt

Node.js Dependencies:

npm install

4. Run the Server
Start the FastAPI application using Uvicorn:

uvicorn app.main:app --host 127.0.0.1 --port 8000

The agent is now running and ready to accept requests.

🛠️ Usage
Interact with the agent by sending a POST request to the /generate endpoint.

Generate Python Tests
curl -X POST \
  -F "language=python" \
  -F "file=@examples/sample_input.py" \
  http://127.0.0.1:8000/generate

Example Successful Response:

{
  "language": "python",
  "message": "Python tests generated and executed successfully",
  "test_file_path": "tests\\tmp_somefile.py",
  "coverage_report": {
    "status": "Success",
    "summary": "10 tests passed.",
    "coverage_percentage": 100.0,
    "full_log": "..."
  }
}

Generate JavaScript Tests
curl -X POST \
  -F "language=javascript" \
  -F "file=@examples/sample_input.js" \
  http://127.0.0.1:8000/generate

Example Successful Response:

{
  "language": "javascript",
  "message": "JavaScript tests generated and executed successfully",
  "test_file_path": "js_tests\\tmp_somefile.test.js",
  "coverage_report": {
    "status": "Success",
    "summary": "8 tests passed out of 8.",
    "coverage_percentage": 100,
    "full_log": { ... }
  }
}

📂 Project Structure
AgentForce_TestGen/
├── app/                  # Core application logic
│   ├── llm.py            # AI interaction, prompts, and schema validation
│   ├── parser.py         # Python code parser (AST)
│   ├── js_parser.py      # JavaScript code parser (AST via Node.js)
│   ├── test_generator.py # Generates pytest files
│   ├── js_test_generator.py # Generates Jest files
│   ├── runner.py         # Executes pytest and handles coverage
│   ├── js_runner.py      # Executes Jest and handles coverage
│   └── main.py           # FastAPI server and endpoints
├── examples/             # Sample code files to test the agent
├── js/                   # Node.js helper scripts for parsing
├── tests/                # Output directory for generated Python tests
├── js_tests/             # Output directory for generated JS tests
├── .gitignore            # Specifies files for Git to ignore
├── requirements.txt      # Python dependencies
└── package.json          # Node.js dependencies
