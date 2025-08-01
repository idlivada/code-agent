import os
import shutil

def copy_directory(source_path: str, destination_path: str, force: bool = False, recursive: bool = True) -> str:
    """Copy a directory. Requires force=True for confirmation. If recursive=True, copies contents too."""
    try:
        # Validate parameters
        if not force:
            raise ValueError("Copying directories requires force=True for safety. Please confirm you want to copy this directory.")
        
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
        
        # Get directory info before copying
        try:
            items = os.listdir(source_path)
            item_count = len(items)
        except PermissionError:
            item_count = "unknown (permission denied)"
        
        # Copy the directory
        if recursive:
            shutil.copytree(source_path, destination_path)
            return f"Successfully copied directory '{source_path}' to '{destination_path}' ({item_count} items)"
        else:
            # Create empty directory
            os.makedirs(destination_path)
            return f"Successfully created empty directory '{destination_path}' (copy of '{source_path}')"
        
    except Exception as e:
        raise Exception(f"Error copying directory from {source_path} to {destination_path}: {str(e)}")

# Tool definition
COPY_DIRECTORY_DEFINITION = {
    "name": "copy_directory",
    "description": "Copy a directory. Requires force=True for confirmation. If recursive=True, copies contents too.",
    "input_schema": {
        "type": "object",
        "properties": {
            "source_path": {
                "type": "string",
                "description": "The path of the directory to copy."
            },
            "destination_path": {
                "type": "string",
                "description": "The destination path for the copied directory."
            },
            "force": {
                "type": "boolean",
                "description": "Must be True to confirm copy operation. This prevents accidental directory copies.",
                "default": False
            },
            "recursive": {
                "type": "boolean",
                "description": "Whether to copy directory contents as well. Defaults to True.",
                "default": True
            }
        },
        "required": ["source_path", "destination_path", "force"],
        "additionalProperties": False
    },
    "tool_function": copy_directory
} 