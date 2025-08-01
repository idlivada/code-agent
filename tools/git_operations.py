import subprocess
import os
import sys
from typing import Optional

def git_operation(operation: str, args: str = "", message: str = "") -> str:
    """Perform various git operations."""
    try:
        # Validate parameters
        if not operation:
            raise ValueError("Git operation cannot be empty")
        
        # Prepare command based on operation
        cmd = ["git"]
        
        if operation == "status":
            cmd.extend(["status"])
        elif operation == "add":
            cmd.extend(["add"])
            if args:
                cmd.extend(args.split())
            else:
                cmd.append(".")
        elif operation == "commit":
            cmd.extend(["commit"])
            if message:
                cmd.extend(["-m", message])
            else:
                cmd.append("-m", "Auto-commit by AI agent")
        elif operation == "diff":
            cmd.extend(["diff"])
            if args:
                cmd.extend(args.split())
        elif operation == "log":
            cmd.extend(["log", "--oneline", "-10"])
            if args:
                cmd.extend(args.split())
        elif operation == "branch":
            cmd.extend(["branch"])
            if args:
                cmd.extend(args.split())
        elif operation == "checkout":
            cmd.extend(["checkout"])
            if args:
                cmd.extend(args.split())
        elif operation == "pull":
            cmd.extend(["pull"])
            if args:
                cmd.extend(args.split())
        elif operation == "push":
            cmd.extend(["push"])
            if args:
                cmd.extend(args.split())
        elif operation == "stash":
            cmd.extend(["stash"])
            if args:
                cmd.extend(args.split())
        elif operation == "stash_pop":
            cmd.extend(["stash", "pop"])
        elif operation == "remote":
            cmd.extend(["remote", "-v"])
        else:
            raise ValueError(f"Unsupported git operation: {operation}")
        
        # Execute git command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.getcwd()
        )
        
        # Format output
        output = []
        output.append(f"🔧 Git operation: {operation}")
        if args:
            output.append(f"📝 Arguments: {args}")
        if message:
            output.append(f"💬 Message: {message}")
        output.append(f"📊 Exit Code: {result.returncode}")
        
        if result.stdout:
            output.append(f"\n📤 STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output.append(f"\n⚠️  STDERR:\n{result.stderr}")
        
        # Interpret results
        if result.returncode == 0:
            output.append(f"\n✅ Git {operation} completed successfully")
        elif result.returncode == 1:
            output.append(f"\n⚠️  Git {operation} completed with warnings")
        else:
            output.append(f"\n❌ Git {operation} failed")
        
        return "\n".join(output)
        
    except subprocess.TimeoutExpired:
        raise Exception(f"Git operation timed out after 60 seconds")
    except Exception as e:
        raise Exception(f"Error performing git {operation}: {str(e)}")

# Tool definition
GIT_OPERATIONS_DEFINITION = {
    "name": "git_operations",
    "description": "Perform various git operations like status, commit, diff, log, branch, etc.",
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "Git operation to perform: 'status', 'add', 'commit', 'diff', 'log', 'branch', 'checkout', 'pull', 'push', 'stash', 'stash_pop', 'remote'."
            },
            "args": {
                "type": "string",
                "description": "Additional arguments for the git operation.",
                "default": ""
            },
            "message": {
                "type": "string",
                "description": "Commit message (for commit operation).",
                "default": ""
            }
        },
        "required": ["operation"],
        "additionalProperties": False
    },
    "tool_function": git_operation
} 