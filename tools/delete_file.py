import os

def delete_file(path: str, force: bool = False) -> str:
    """Delete a file. Requires force=True for confirmation to prevent accidental deletions."""
    try:
        # Validate parameters
        if not force:
            raise ValueError("Deleting files requires force=True for safety. Please confirm you want to delete this file.")
        
        # Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"File '{path}' not found")
        
        # Check if it's actually a file (not a directory)
        if not os.path.isfile(path):
            raise ValueError(f"'{path}' is not a file (it's a directory)")
        
        # Get file info before deletion
        file_size = os.path.getsize(path)
        
        # Delete the file
        os.remove(path)
        
        return f"Successfully deleted file '{path}' ({file_size} bytes)"
        
    except Exception as e:
        raise Exception(f"Error deleting file {path}: {str(e)}")

# Tool definition
DELETE_FILE_DEFINITION = {
    "name": "delete_file",
    "description": "Delete a file. Requires force=True for confirmation to prevent accidental deletions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the file to delete."
            },
            "force": {
                "type": "boolean",
                "description": "Must be True to confirm deletion. This prevents accidental file deletions.",
                "default": False
            }
        },
        "required": ["path", "force"],
        "additionalProperties": False
    },
    "tool_function": delete_file
} 