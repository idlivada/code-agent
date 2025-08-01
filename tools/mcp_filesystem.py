import subprocess
import json
import os
from typing import Dict, Any, Optional

def mcp_filesystem_operation(operation: str, path: str = "", content: str = "", destination: str = "") -> str:
    """Perform filesystem operations using the MCP filesystem server."""
    try:
        # Validate parameters
        if not operation:
            raise ValueError("Operation cannot be empty")
        
        # This is a placeholder for MCP filesystem integration
        # In a real implementation, this would communicate with the MCP filesystem server
        # For now, we'll simulate the operations using local file system
        
        if operation == "read_file":
            if not path:
                raise ValueError("Path is required for read_file operation")
            
            if not os.path.exists(path):
                raise FileNotFoundError(f"File '{path}' not found")
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"📄 Read file '{path}':\n{content}"
            
        elif operation == "write_file":
            if not path:
                raise ValueError("Path is required for write_file operation")
            if content is None:
                raise ValueError("Content is required for write_file operation")
            
            # Ensure directory exists
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ Wrote {len(content)} characters to file '{path}'"
            
        elif operation == "delete_file":
            if not path:
                raise ValueError("Path is required for delete_file operation")
            
            if not os.path.exists(path):
                raise FileNotFoundError(f"File '{path}' not found")
            
            os.remove(path)
            return f"🗑️  Deleted file '{path}'"
            
        elif operation == "list_directory":
            if not path:
                path = "."
            
            if not os.path.exists(path):
                raise FileNotFoundError(f"Directory '{path}' not found")
            
            if not os.path.isdir(path):
                raise ValueError(f"'{path}' is not a directory")
            
            items = os.listdir(path)
            files = []
            directories = []
            
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    directories.append(item + "/")
                else:
                    files.append(item)
            
            result = [f"📁 Directory listing for '{path}':"]
            if directories:
                result.append("📁 Directories:")
                for directory in sorted(directories):
                    result.append(f"  {directory}")
            
            if files:
                result.append("📄 Files:")
                for file in sorted(files):
                    result.append(f"  {file}")
            
            if not directories and not files:
                result.append("(empty directory)")
            
            return "\n".join(result)
            
        elif operation == "create_directory":
            if not path:
                raise ValueError("Path is required for create_directory operation")
            
            if os.path.exists(path):
                if os.path.isdir(path):
                    return f"📁 Directory '{path}' already exists"
                else:
                    raise ValueError(f"'{path}' exists but is not a directory")
            
            os.makedirs(path, exist_ok=True)
            return f"📁 Created directory '{path}'"
            
        elif operation == "delete_directory":
            if not path:
                raise ValueError("Path is required for delete_directory operation")
            
            if not os.path.exists(path):
                raise FileNotFoundError(f"Directory '{path}' not found")
            
            if not os.path.isdir(path):
                raise ValueError(f"'{path}' is not a directory")
            
            import shutil
            shutil.rmtree(path)
            return f"🗑️  Deleted directory '{path}' and all contents"
            
        elif operation == "move_file":
            if not path:
                raise ValueError("Source path is required for move_file operation")
            if not destination:
                raise ValueError("Destination path is required for move_file operation")
            
            if not os.path.exists(path):
                raise FileNotFoundError(f"Source file '{path}' not found")
            
            import shutil
            shutil.move(path, destination)
            return f"📦 Moved '{path}' to '{destination}'"
            
        elif operation == "copy_file":
            if not path:
                raise ValueError("Source path is required for copy_file operation")
            if not destination:
                raise ValueError("Destination path is required for copy_file operation")
            
            if not os.path.exists(path):
                raise FileNotFoundError(f"Source file '{path}' not found")
            
            import shutil
            shutil.copy2(path, destination)
            return f"📋 Copied '{path}' to '{destination}'"
            
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
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