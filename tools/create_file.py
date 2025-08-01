import os

def create_file(path: str, content: str = "", overwrite: bool = False) -> str:
    """Create a new file with specified content. If the file already exists, it will only be overwritten if overwrite is True."""
    try:
        # Check if file already exists
        if os.path.exists(path) and not overwrite:
            raise FileExistsError(f"File '{path}' already exists. Set overwrite=True to overwrite it.")
        
        # Ensure the directory exists
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create the file with content
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        if os.path.exists(path) and not overwrite:
            return f"Created new file '{path}' with {len(content)} characters"
        else:
            return f"Overwrote file '{path}' with {len(content)} characters"
            
    except Exception as e:
        raise Exception(f"Error creating file {path}: {str(e)}")

# Tool definition
CREATE_FILE_DEFINITION = {
    "name": "create_file",
    "description": "Create a new file with specified content. If the file already exists, it will only be overwritten if overwrite is True.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the file to create."
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file. Defaults to empty string.",
                "default": ""
            },
            "overwrite": {
                "type": "boolean",
                "description": "Whether to overwrite existing files. Defaults to False.",
                "default": False
            }
        },
        "required": ["path"],
        "additionalProperties": False
    },
    "tool_function": create_file
} 