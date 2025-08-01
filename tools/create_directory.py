import os

def create_directory(path: str, create_parents: bool = True) -> str:
    """Create a directory. If create_parents is True, creates parent directories as needed."""
    try:
        # Validate parameters
        if not path:
            raise ValueError("Directory path cannot be empty")
        
        # Check if directory already exists
        if os.path.exists(path):
            if os.path.isdir(path):
                return f"Directory '{path}' already exists"
            else:
                raise ValueError(f"'{path}' exists but is not a directory")
        
        # Create directory
        if create_parents:
            os.makedirs(path, exist_ok=True)
            return f"Created directory '{path}' (including parent directories if needed)"
        else:
            os.mkdir(path)
            return f"Created directory '{path}'"
            
    except Exception as e:
        raise Exception(f"Error creating directory {path}: {str(e)}")

# Tool definition
CREATE_DIRECTORY_DEFINITION = {
    "name": "create_directory",
    "description": "Create a directory. If create_parents is True, creates parent directories as needed.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the directory to create."
            },
            "create_parents": {
                "type": "boolean",
                "description": "Whether to create parent directories if they don't exist. Defaults to True.",
                "default": True
            }
        },
        "required": ["path"],
        "additionalProperties": False
    },
    "tool_function": create_directory
} 