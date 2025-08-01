import json
import os
from typing import Dict, Any, Optional
from .mcp_client import create_filesystem_client

def mcp_filesystem_operation(operation: str, path: str = "", content: str = "", destination: str = "") -> str:
    """Perform filesystem operations using the MCP filesystem server."""
    try:
        # Validate parameters
        if not operation:
            raise ValueError("Operation cannot be empty")
        
        # Create MCP client
        client = create_filesystem_client()
        
        # Prepare arguments based on operation
        arguments = {}
        
        if operation == "read_file":
            if not path:
                raise ValueError("Path is required for read_file operation")
            arguments = {"path": path}
            
        elif operation == "write_file":
            if not path:
                raise ValueError("Path is required for write_file operation")
            if content is None:
                raise ValueError("Content is required for write_file operation")
            arguments = {"path": path, "content": content}
            
        elif operation == "delete_file":
            if not path:
                raise ValueError("Path is required for delete_file operation")
            arguments = {"path": path}
            
        elif operation == "list_directory":
            if not path:
                path = "."
            arguments = {"path": path}
            
        elif operation == "create_directory":
            if not path:
                raise ValueError("Path is required for create_directory operation")
            arguments = {"path": path}
            
        elif operation == "delete_directory":
            if not path:
                raise ValueError("Path is required for delete_directory operation")
            arguments = {"path": path}
            
        elif operation == "move_file":
            if not path:
                raise ValueError("Source path is required for move_file operation")
            if not destination:
                raise ValueError("Destination path is required for move_file operation")
            arguments = {"source": path, "destination": destination}
            
        elif operation == "copy_file":
            if not path:
                raise ValueError("Source path is required for copy_file operation")
            if not destination:
                raise ValueError("Destination path is required for copy_file operation")
            arguments = {"source": path, "destination": destination}
            
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        # Call the MCP server
        result = client.call_tool(operation, arguments)
        return f"✅ MCP {operation} completed successfully:\n{result}"
        
    except Exception as e:
        raise Exception(f"Error in MCP filesystem operation '{operation}': {str(e)}")

# Tool definition
MCP_FILESYSTEM_DEFINITION = {
    "name": "mcp_filesystem",
    "description": "Perform filesystem operations using the MCP filesystem server (read_file, write_file, delete_file, list_directory, create_directory, delete_directory, move_file, copy_file).",
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "The filesystem operation to perform: 'read_file', 'write_file', 'delete_file', 'list_directory', 'create_directory', 'delete_directory', 'move_file', 'copy_file'."
            },
            "path": {
                "type": "string",
                "description": "The file or directory path for the operation."
            },
            "content": {
                "type": "string",
                "description": "Content to write (for write_file operation)."
            },
            "destination": {
                "type": "string",
                "description": "Destination path (for move_file and copy_file operations)."
            }
        },
        "required": ["operation"],
        "additionalProperties": False
    },
    "tool_function": mcp_filesystem_operation
} 