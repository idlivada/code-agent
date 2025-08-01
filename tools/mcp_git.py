import json
import os
from typing import Dict, Any, Optional
from .mcp_client import create_git_client

def mcp_git_operation(operation: str, args: str = "", message: str = "", force: bool = False) -> str:
    """Perform git operations using the MCP git server."""
    try:
        # Validate parameters
        if not operation:
            raise ValueError("Git operation cannot be empty")
        
        # Create MCP client
        client = create_git_client()
        
        # Prepare arguments based on operation
        arguments = {}
        
        if operation == "status":
            arguments = {}
            
        elif operation == "add":
            if args:
                arguments = {"paths": args.split()}
            else:
                arguments = {"paths": ["."]}
                
        elif operation == "commit":
            if message:
                arguments = {"message": message}
            else:
                arguments = {"message": "Auto-commit by AI agent"}
                
        elif operation == "diff":
            if args:
                arguments = {"args": args.split()}
            else:
                arguments = {}
                
        elif operation == "log":
            if args:
                arguments = {"args": args.split()}
            else:
                arguments = {"args": ["--oneline", "-10"]}
                
        elif operation == "branch":
            if args:
                arguments = {"args": args.split()}
            else:
                arguments = {}
                
        elif operation == "checkout":
            if args:
                arguments = {"args": args.split()}
            else:
                raise ValueError("Branch or path required for checkout operation")
                
        elif operation == "pull":
            if args:
                arguments = {"args": args.split()}
            else:
                arguments = {}
                
        elif operation == "push":
            if args:
                arguments = {"args": args.split()}
            else:
                arguments = {}
                
        elif operation == "stash":
            if args:
                arguments = {"args": args.split()}
            else:
                arguments = {}
                
        elif operation == "stash_pop":
            arguments = {}
            
        elif operation == "remote":
            arguments = {}
            
        elif operation == "clone":
            if not args:
                raise ValueError("Repository URL is required for clone operation")
            arguments = {"url": args}
            
        elif operation == "init":
            if args:
                arguments = {"args": args.split()}
            else:
                arguments = {}
                
        elif operation == "merge":
            if args:
                arguments = {"args": args.split()}
            else:
                raise ValueError("Branch required for merge operation")
                
        elif operation == "rebase":
            if args:
                arguments = {"args": args.split()}
            else:
                raise ValueError("Branch required for rebase operation")
                
        elif operation == "reset":
            if args:
                arguments = {"args": args.split()}
            else:
                raise ValueError("Reset target required")
                
        elif operation == "clean":
            clean_args = []
            if force:
                clean_args.append("-f")
            if args:
                clean_args.extend(args.split())
            arguments = {"args": clean_args}
            
        else:
            raise ValueError(f"Unsupported git operation: {operation}")
        
        # Call the MCP server
        result = client.call_tool(operation, arguments)
        return f"✅ MCP git {operation} completed successfully:\n{result}"
        
    except Exception as e:
        raise Exception(f"Error performing MCP git {operation}: {str(e)}")

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