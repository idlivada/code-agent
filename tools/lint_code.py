import subprocess
import os
import sys
from typing import Optional

def lint_code(path: str = ".", linter: str = "flake8", args: str = "", fix: bool = False) -> str:
    """Run code linting and formatting tools."""
    try:
        # Validate parameters
        if not path:
            raise ValueError("Path cannot be empty")
        
        # Check if path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path '{path}' not found")
        
        # Prepare command based on linter
        if linter.lower() == "flake8":
            cmd = [sys.executable, "-m", "flake8", path]
            if args:
                cmd.extend(args.split())
        elif linter.lower() == "pylint":
            cmd = [sys.executable, "-m", "pylint", path]
            if args:
                cmd.extend(args.split())
        elif linter.lower() == "black":
            cmd = [sys.executable, "-m", "black", path]
            if not fix:
                cmd.append("--check")
            if args:
                cmd.extend(args.split())
        elif linter.lower() == "isort":
            cmd = [sys.executable, "-m", "isort", path]
            if not fix:
                cmd.append("--check-only")
            if args:
                cmd.extend(args.split())
        elif linter.lower() == "autopep8":
            cmd = [sys.executable, "-m", "autopep8", path]
            if not fix:
                cmd.append("--diff")
            if args:
                cmd.extend(args.split())
        else:
            raise ValueError(f"Unsupported linter: {linter}. Use 'flake8', 'pylint', 'black', 'isort', or 'autopep8'")
        
        # Execute linter
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.getcwd()
        )
        
        # Format output
        output = []
        output.append(f"🔍 Running {linter} on {path}")
        output.append(f"🔧 Fix mode: {fix}")
        output.append(f"📊 Exit Code: {result.returncode}")
        
        if result.stdout:
            output.append(f"\n📤 STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output.append(f"\n⚠️  STDERR:\n{result.stderr}")
        
        # Interpret results
        if result.returncode == 0:
            output.append(f"\n✅ Code passed {linter} checks!")
        elif result.returncode == 1:
            output.append(f"\n⚠️  {linter} found issues")
        elif result.returncode == 2:
            output.append(f"\n❌ {linter} execution error")
        else:
            output.append(f"\n❓ Unexpected exit code: {result.returncode}")
        
        return "\n".join(output)
        
    except subprocess.TimeoutExpired:
        raise Exception(f"Linting timed out after 120 seconds")
    except Exception as e:
        raise Exception(f"Error running {linter}: {str(e)}")

# Tool definition
LINT_CODE_DEFINITION = {
    "name": "lint_code",
    "description": "Run code linting and formatting tools like flake8, pylint, black, isort, or autopep8.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to lint (file or directory). Defaults to current directory.",
                "default": "."
            },
            "linter": {
                "type": "string",
                "description": "Linter to use: 'flake8', 'pylint', 'black', 'isort', or 'autopep8'. Defaults to 'flake8'.",
                "default": "flake8"
            },
            "args": {
                "type": "string",
                "description": "Additional arguments to pass to the linter.",
                "default": ""
            },
            "fix": {
                "type": "boolean",
                "description": "Whether to fix issues automatically (for formatters). Defaults to False.",
                "default": False
            }
        },
        "required": [],
        "additionalProperties": False
    },
    "tool_function": lint_code
} 