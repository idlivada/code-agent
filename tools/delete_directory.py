import os
import shutil

def delete_directory(path: str, force: bool = False, recursive: bool = False) -> str:
    """Delete a directory. Requires force=True for confirmation. If recursive=True, deletes contents too."""
    try:
        # Validate parameters
        if not force:
            raise ValueError("Deleting directories requires force=True for safety. Please confirm you want to delete this directory.")
        
        # Check if directory exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory '{path}' not found")
        
        # Check if it's actually a directory
        if not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a directory")
        
        # Get directory info before deletion
        try:
            items = os.listdir(path)
            item_count = len(items)
        except PermissionError:
            item_count = "unknown (permission denied)"
        
        # Check if directory is empty
        if not recursive and item_count > 0:
            raise ValueError(f"Directory '{path}' is not empty ({item_count} items). Use recursive=True to delete non-empty directories.")
        
        # Delete the directory
        if recursive:
            shutil.rmtree(path)
            return f"Successfully deleted directory '{path}' and all its contents ({item_count} items)"
        else:
            os.rmdir(path)
            return f"Successfully deleted empty directory '{path}'"
        
    except Exception as e:
        raise Exception(f"Error deleting directory {path}: {str(e)}")

# Tool definition
DELETE_DIRECTORY_DEFINITION = {
    "name": "delete_directory",
    "description": "Delete a directory. Requires force=True for confirmation. If recursive=True, deletes contents too.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the directory to delete."
            },
            "force": {
                "type": "boolean",
                "description": "Must be True to confirm deletion. This prevents accidental directory deletions.",
                "default": False
            },
            "recursive": {
                "type": "boolean",
                "description": "Whether to delete directory contents as well. Required for non-empty directories.",
                "default": False
            }
        },
        "required": ["path", "force"],
        "additionalProperties": False
    },
    "tool_function": delete_directory
} 