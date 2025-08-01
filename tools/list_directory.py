import os
import json

def list_directory(path: str = ".") -> str:
    """List the contents of a directory at the given path."""
    try:
        # Ensure the path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found: {path}")
        
        # Check if it's actually a directory
        if not os.path.isdir(path):
            raise ValueError(f"Path is not a directory: {path}")
        
        # Get directory contents
        items = os.listdir(path)
        
        # Separate files and directories
        files = []
        directories = []
        
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                directories.append(item + "/")
            else:
                files.append(item)
        
        # Sort both lists
        directories.sort()
        files.sort()
        
        # Build the result
        result = []
        if directories:
            result.append("Directories:")
            for directory in directories:
                result.append(f"  {directory}")
        
        if files:
            if result:  # Add a blank line if we already have directories
                result.append("")
            result.append("Files:")
            for file in files:
                result.append(f"  {file}")
        
        if not result:
            result.append("(empty directory)")
        
        return "\n".join(result)
        
    except Exception as e:
        raise Exception(f"Error listing directory {path}: {str(e)}")

# Tool definition
LIST_DIRECTORY_DEFINITION = {
    "name": "list_directory",
    "description": "List the contents of a directory at the given path. Use this when you want to see what files and folders are in a directory.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to the directory to list. Defaults to current directory ('.') if not specified.",
                "default": "."
            }
        },
        "required": [],
        "additionalProperties": False
    },
    "tool_function": list_directory
} 