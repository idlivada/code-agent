import os

def edit_file(path: str, old_str: str, new_str: str) -> str:
    """Replace 'old_str' with 'new_str' in the given file. If the file doesn't exist, it will be created."""
    try:
        # Validate required parameters
        if path is None or path == "":
            raise ValueError("path parameter is required")
        if old_str is None:
            raise ValueError("old_str parameter is required")
        if new_str is None:
            raise ValueError("new_str parameter is required")
        
        # Ensure old_str and new_str are different
        if old_str == new_str:
            raise ValueError("old_str and new_str must be different from each other")
        
        # Check if file exists
        file_exists = os.path.exists(path)
        
        if file_exists:
            # Read the existing file
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check if old_str exists in the file
            if old_str not in content:
                raise ValueError(f"String '{old_str}' not found in file '{path}'")
            
            # Replace the old string with the new string
            new_content = content.replace(old_str, new_str)
            
            # Write the updated content back to the file
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            return f"Successfully replaced '{old_str}' with '{new_str}' in file '{path}'"
        else:
            # Create new file with new_str as content
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_str)
            
            return f"Created new file '{path}' with content '{new_str}'"
            
    except Exception as e:
        raise Exception(f"Error editing file {path}: {str(e)}")

# Tool definition
EDIT_FILE_DEFINITION = {
    "name": "edit_file",
    "description": "Replace 'old_str' with 'new_str' in the given file. If the file doesn't exist, it will be created with 'new_str' as content. old_str and new_str must be different from each other.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the file to edit or create."
            },
            "old_str": {
                "type": "string",
                "description": "The string to replace. Must be different from new_str."
            },
            "new_str": {
                "type": "string",
                "description": "The string to replace old_str with. Must be different from old_str."
            }
        },
        "required": ["path", "old_str", "new_str"],
        "additionalProperties": False
    },
    "tool_function": edit_file
} 