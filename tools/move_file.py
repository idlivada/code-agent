import os
import shutil

def move_file(source_path: str, destination_path: str, force: bool = False) -> str:
    """Move or rename a file. Requires force=True for confirmation to prevent accidental moves."""
    try:
        # Validate parameters
        if not force:
            raise ValueError("Moving files requires force=True for safety. Please confirm you want to move this file.")
        
        # Check if source file exists
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file '{source_path}' not found")
        
        # Check if it's actually a file (not a directory)
        if not os.path.isfile(source_path):
            raise ValueError(f"'{source_path}' is not a file (it's a directory)")
        
        # Check if destination already exists
        if os.path.exists(destination_path):
            raise FileExistsError(f"Destination '{destination_path}' already exists. Use force=True to overwrite.")
        
        # Ensure the destination directory exists
        destination_dir = os.path.dirname(destination_path)
        if destination_dir and not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Get file info before moving
        file_size = os.path.getsize(source_path)
        
        # Move the file
        shutil.move(source_path, destination_path)
        
        return f"Successfully moved '{source_path}' to '{destination_path}' ({file_size} bytes)"
        
    except Exception as e:
        raise Exception(f"Error moving file from {source_path} to {destination_path}: {str(e)}")

# Tool definition
MOVE_FILE_DEFINITION = {
    "name": "move_file",
    "description": "Move or rename a file. Requires force=True for confirmation to prevent accidental moves.",
    "input_schema": {
        "type": "object",
        "properties": {
            "source_path": {
                "type": "string",
                "description": "The path of the file to move."
            },
            "destination_path": {
                "type": "string",
                "description": "The destination path for the file."
            },
            "force": {
                "type": "boolean",
                "description": "Must be True to confirm move operation. This prevents accidental file moves.",
                "default": False
            }
        },
        "required": ["source_path", "destination_path", "force"],
        "additionalProperties": False
    },
    "tool_function": move_file
} 