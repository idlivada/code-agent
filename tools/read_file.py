import json

def read_file(path: str) -> str:
    """Read the contents of a given relative file path."""
    try:        
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

# Tool definition
READ_FILE_DEFINITION = {
    "name": "read_file",
    "description": "Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The relative path of a file in the working directory."
            }
        },
        "required": ["path"],
        "additionalProperties": False
    },
    "tool_function": read_file
}