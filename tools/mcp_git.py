import subprocess
import json
import os
from typing import Dict, Any, Optional

def mcp_git_operation(operation: str, args: str = "", message: str = "", force: bool = False) -> str:
    """Perform git operations using the MCP git server."""
    try:
        # Validate parameters
        if not operation:
            raise ValueError("Git operation cannot be empty")
        
        # This is a placeholder for MCP git integration
        # In a real implementation, this would communicate with the MCP git server
        # For now, we'll simulate the operations using local git commands
        
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
        elif operation == "clone":
            if not args:
                raise ValueError("Repository URL is required for clone operation")
            cmd.extend(["clone", args])
        elif operation == "init":
            cmd.extend(["init"])
            if args:
                cmd.extend(args.split())
        elif operation == "merge":
            cmd.extend(["merge"])
            if args:
                cmd.extend(args.split())
        elif operation == "rebase":
            cmd.extend(["rebase"])
            if args:
                cmd.extend(args.split())
        elif operation == "reset":
            cmd.extend(["reset"])
            if args:
                cmd.extend(args.split())
        elif operation == "clean":
            cmd.extend(["clean"])
            if force:
                cmd.append("-f")
            if args:
                cmd.extend(args.split())
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
        if force:
            output.append(f"⚠️  Force mode: enabled")
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
MCP_GIT_DEFINITION = {
    "name": "mcp_git",
    "description": "Perform git operations using the MCP git server (status, add, commit, diff, log, branch, checkout, pull, push, stash, clone, init, merge, rebase, reset, clean).",
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "Git operation to perform: 'status', 'add', 'commit', 'diff', 'log', 'branch', 'checkout', 'pull', 'push', 'stash', 'stash_pop', 'remote', 'clone', 'init', 'merge', 'rebase', 'reset', 'clean'."
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
            },
            "force": {
                "type": "boolean",
                "description": "Force mode for destructive operations (clean, reset --hard, etc.).",
                "default": False
            }
        },
        "required": ["operation"],
        "additionalProperties": False
    },
    "tool_function": mcp_git_operation
} 