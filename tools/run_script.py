import subprocess
import sys
import os
from typing import Optional

def run_script(script_path: str, args: str = "", timeout: int = 30, capture_output: bool = True) -> str:
    """Execute a Python script and capture its output and errors."""
    try:
        # Validate parameters
        if not script_path:
            raise ValueError("Script path cannot be empty")
        
        # Check if script exists
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script '{script_path}' not found")
        
        # Check if it's actually a file
        if not os.path.isfile(script_path):
            raise ValueError(f"'{script_path}' is not a file")
        
        # Prepare command
        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args.split())
        
        # Execute the script
        if capture_output:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd()
            )
            
            # Format output
            output = []
            output.append(f"🚀 Executed: {' '.join(cmd)}")
            output.append(f"⏱️  Timeout: {timeout}s")
            output.append(f"📊 Exit Code: {result.returncode}")
            
            if result.stdout:
                output.append(f"\n📤 STDOUT:\n{result.stdout}")
            
            if result.stderr:
                output.append(f"\n⚠️  STDERR:\n{result.stderr}")
            
            if result.returncode != 0:
                output.append(f"\n❌ Script failed with exit code {result.returncode}")
            else:
                output.append(f"\n✅ Script executed successfully")
            
            return "\n".join(output)
        else:
            # Run without capturing output (for interactive scripts)
            result = subprocess.run(
                cmd,
                timeout=timeout,
                cwd=os.getcwd()
            )
            
            return f"🚀 Executed: {' '.join(cmd)}\n📊 Exit Code: {result.returncode}"
            
    except subprocess.TimeoutExpired:
        raise Exception(f"Script execution timed out after {timeout} seconds")
    except Exception as e:
        raise Exception(f"Error executing script {script_path}: {str(e)}")

# Tool definition
RUN_SCRIPT_DEFINITION = {
    "name": "run_script",
    "description": "Execute a Python script and capture its output and errors.",
    "input_schema": {
        "type": "object",
        "properties": {
            "script_path": {
                "type": "string",
                "description": "The path to the Python script to execute."
            },
            "args": {
                "type": "string",
                "description": "Command line arguments to pass to the script.",
                "default": ""
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds for script execution. Defaults to 30.",
                "default": 30
            },
            "capture_output": {
                "type": "boolean",
                "description": "Whether to capture and return script output. Defaults to True.",
                "default": True
            }
        },
        "required": ["script_path"],
        "additionalProperties": False
    },
    "tool_function": run_script
} 