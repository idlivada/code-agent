import subprocess
import os
import sys
from typing import Optional

def check_security(path: str = ".", scanner: str = "bandit", args: str = "") -> str:
    """Run security scanners to check for vulnerabilities and security issues."""
    try:
        # Validate parameters
        if not path:
            raise ValueError("Path cannot be empty")
        
        # Check if path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path '{path}' not found")
        
        # Prepare command based on scanner
        if scanner.lower() == "bandit":
            cmd = [sys.executable, "-m", "bandit", "-r", path]
            if args:
                cmd.extend(args.split())
        elif scanner.lower() == "safety":
            cmd = [sys.executable, "-m", "safety", "check"]
            if args:
                cmd.extend(args.split())
        elif scanner.lower() == "pip-audit":
            cmd = [sys.executable, "-m", "pip_audit"]
            if args:
                cmd.extend(args.split())
        else:
            raise ValueError(f"Unsupported security scanner: {scanner}. Use 'bandit', 'safety', or 'pip-audit'")
        
        # Execute security scan
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.getcwd()
        )
        
        # Format output
        output = []
        output.append(f"🔒 Running {scanner} security scan on {path}")
        output.append(f"📊 Exit Code: {result.returncode}")
        
        if result.stdout:
            output.append(f"\n📤 STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output.append(f"\n⚠️  STDERR:\n{result.stderr}")
        
        # Interpret results
        if result.returncode == 0:
            output.append(f"\n✅ Security scan passed - no issues found")
        elif result.returncode == 1:
            output.append(f"\n⚠️  Security scan found issues")
        elif result.returncode == 2:
            output.append(f"\n❌ Security scan failed to execute")
        else:
            output.append(f"\n❓ Unexpected exit code: {result.returncode}")
        
        return "\n".join(output)
        
    except subprocess.TimeoutExpired:
        raise Exception(f"Security scan timed out after 120 seconds")
    except Exception as e:
        raise Exception(f"Error running security scan: {str(e)}")

# Tool definition
CHECK_SECURITY_DEFINITION = {
    "name": "check_security",
    "description": "Run security scanners like bandit, safety, or pip-audit to check for vulnerabilities.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to scan (file or directory). Defaults to current directory.",
                "default": "."
            },
            "scanner": {
                "type": "string",
                "description": "Security scanner to use: 'bandit', 'safety', or 'pip-audit'. Defaults to 'bandit'.",
                "default": "bandit"
            },
            "args": {
                "type": "string",
                "description": "Additional arguments to pass to the security scanner.",
                "default": ""
            }
        },
        "required": [],
        "additionalProperties": False
    },
    "tool_function": check_security
} 