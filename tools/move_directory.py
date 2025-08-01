import os
import shutil

def move_directory(source_path: str, destination_path: str, force: bool = False) -> str:
    """Move or rename a directory. Requires force=True for confirmation to prevent accidental moves."""
    try:
        # Validate parameters
        if not force:
            raise ValueError("Moving directories requires force=True for safety. Please confirm you want to move this directory.")
        
        # Check if source directory exists
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source directory '{source_path}' not found")
        
        # Check if it's actually a directory
        if not os.path.isdir(source_path):
            raise ValueError(f"'{source_path}' is not a directory")
        
        # Check if destination already exists
        if os.path.exists(destination_path):
            raise FileExistsError(f"Destination '{destination_path}' already exists. Use force=True to overwrite.")
        
        # Ensure the destination parent directory exists
        destination_parent = os.path.dirname(destination_path)
        if destination_parent and not os.path.exists(destination_parent):
            os.makedirs(destination_parent)
        
        # Get directory info before moving
        try:
            items = os.listdir(source_path)
            item_count = len(items)
        except PermissionError:
            item_count = "unknown (permission denied)"
        
        # Move the directory
        shutil.move(source_path, destination_path)
        
        return f"Successfully moved directory '{source_path}' to '{destination_path}' ({item_count} items)"
        
    except Exception as e:
        raise Exception(f"Error moving directory from {source_path} to {destination_path}: {str(e)}")

# Tool definition
MOVE_DIRECTORY_DEFINITION = {
    "name": "move_directory",
    "description": "Move or rename a directory. Requires force=True for confirmation to prevent accidental moves.",
    "input_schema": {
        "type": "object",
        "properties": {
            "source_path": {
                "type": "string",
                "description": "The path of the directory to move."
            },
            "destination_path": {
                "type": "string",
                "description": "The destination path for the directory."
            },
            "force": {
                "type": "boolean",
                "description": "Must be True to confirm move operation. This prevents accidental directory moves.",
                "default": False
            }
        },
        "required": ["source_path", "destination_path", "force"],
        "additionalProperties": False
    },
    "tool_function": move_directory
} 