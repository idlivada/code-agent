import subprocess
import os
import sys
from typing import Optional

def run_tests(test_path: str = ".", framework: str = "pytest", args: str = "", timeout: int = 60) -> str:
    """Run Python tests using pytest or unittest framework."""
    try:
        # Validate parameters
        if not test_path:
            raise ValueError("Test path cannot be empty")
        
        # Check if test path exists
        if not os.path.exists(test_path):
            raise FileNotFoundError(f"Test path '{test_path}' not found")
        
        # Prepare command based on framework
        if framework.lower() == "pytest":
            cmd = [sys.executable, "-m", "pytest", test_path]
            if args:
                cmd.extend(args.split())
        elif framework.lower() == "unittest":
            cmd = [sys.executable, "-m", "unittest", "discover", "-s", test_path]
            if args:
                cmd.extend(args.split())
        else:
            raise ValueError(f"Unsupported test framework: {framework}. Use 'pytest' or 'unittest'")
        
        # Execute tests
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()
        )
        
        # Format output
        output = []
        output.append(f"🧪 Running tests with {framework}")
        output.append(f"📁 Test path: {test_path}")
        output.append(f"⏱️  Timeout: {timeout}s")
        output.append(f"📊 Exit Code: {result.returncode}")
        
        if result.stdout:
            output.append(f"\n📤 STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output.append(f"\n⚠️  STDERR:\n{result.stderr}")
        
        # Interpret results
        if result.returncode == 0:
            output.append(f"\n✅ All tests passed!")
        elif result.returncode == 1:
            output.append(f"\n❌ Some tests failed")
        elif result.returncode == 2:
            output.append(f"\n⚠️  Test execution error")
        else:
            output.append(f"\n❓ Unexpected exit code: {result.returncode}")
        
        return "\n".join(output)
        
    except subprocess.TimeoutExpired:
        raise Exception(f"Test execution timed out after {timeout} seconds")
    except Exception as e:
        raise Exception(f"Error running tests: {str(e)}")

# Tool definition
RUN_TESTS_DEFINITION = {
    "name": "run_tests",
    "description": "Run Python tests using pytest or unittest framework.",
    "input_schema": {
        "type": "object",
        "properties": {
            "test_path": {
                "type": "string",
                "description": "The path to tests (file, directory, or pattern). Defaults to current directory.",
                "default": "."
            },
            "framework": {
                "type": "string",
                "description": "Test framework to use: 'pytest' or 'unittest'. Defaults to 'pytest'.",
                "default": "pytest"
            },
            "args": {
                "type": "string",
                "description": "Additional arguments to pass to the test runner.",
                "default": ""
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds for test execution. Defaults to 60.",
                "default": 60
            }
        },
        "required": [],
        "additionalProperties": False
    },
    "tool_function": run_tests
} 