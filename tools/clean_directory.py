import os
import shutil

def clean_directory(path: str, force: bool = False, remove_empty: bool = True, remove_temp: bool = True) -> str:
    """Clean a directory by removing temporary files and empty directories. Requires force=True for confirmation."""
    try:
        # Validate parameters
        if not force:
            raise ValueError("Cleaning directories requires force=True for safety. Please confirm you want to clean this directory.")
        
        # Check if directory exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory '{path}' not found")
        
        # Check if it's actually a directory
        if not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a directory")
        
        # Define temporary file patterns
        temp_patterns = [
            '*.tmp', '*.temp', '*.bak', '*.backup',
            '*.log', '*.cache', '*.pyc', '__pycache__',
            '.DS_Store', 'Thumbs.db', '*.swp', '*.swo'
        ]
        
        removed_files = []
        removed_dirs = []
        
        # Walk through directory
        for root, dirs, files in os.walk(path, topdown=False):
            # Remove temporary files
            if remove_temp:
                for file in files:
                    file_path = os.path.join(root, file)
                    is_temp = False
                    
                    # Check if file matches temp patterns
                    for pattern in temp_patterns:
                        if pattern.startswith('*'):
                            if file.endswith(pattern[1:]):
                                is_temp = True
                                break
                        elif pattern == '__pycache__':
                            if file == '__pycache__':
                                is_temp = True
                                break
                        elif pattern in ['.DS_Store', 'Thumbs.db']:
                            if file == pattern:
                                is_temp = True
                                break
                        elif pattern.startswith('*.') and file.endswith(pattern[1:]):
                            is_temp = True
                            break
                    
                    if is_temp:
                        try:
                            os.remove(file_path)
                            removed_files.append(file_path)
                        except (PermissionError, OSError):
                            pass
            
            # Remove empty directories
            if remove_empty:
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        if not os.listdir(dir_path):  # Directory is empty
                            os.rmdir(dir_path)
                            removed_dirs.append(dir_path)
                    except (PermissionError, OSError):
                        pass
        
        # Format result
        result = [f"🧹 Cleaned directory: {path}"]
        
        if removed_files:
            result.append(f"🗑️  Removed {len(removed_files)} temporary files:")
            for file in removed_files[:10]:  # Show first 10
                result.append(f"  - {os.path.relpath(file, path)}")
            if len(removed_files) > 10:
                result.append(f"  ... and {len(removed_files) - 10} more")
        
        if removed_dirs:
            result.append(f"📁 Removed {len(removed_dirs)} empty directories:")
            for dir_path in removed_dirs[:10]:  # Show first 10
                result.append(f"  - {os.path.relpath(dir_path, path)}")
            if len(removed_dirs) > 10:
                result.append(f"  ... and {len(removed_dirs) - 10} more")
        
        if not removed_files and not removed_dirs:
            result.append("✨ Directory was already clean!")
        
        return "\n".join(result)
        
    except Exception as e:
        raise Exception(f"Error cleaning directory {path}: {str(e)}")

# Tool definition
CLEAN_DIRECTORY_DEFINITION = {
    "name": "clean_directory",
    "description": "Clean a directory by removing temporary files and empty directories. Requires force=True for confirmation.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the directory to clean."
            },
            "force": {
                "type": "boolean",
                "description": "Must be True to confirm cleaning operation. This prevents accidental file deletions.",
                "default": False
            },
            "remove_empty": {
                "type": "boolean",
                "description": "Whether to remove empty directories. Defaults to True.",
                "default": True
            },
            "remove_temp": {
                "type": "boolean",
                "description": "Whether to remove temporary files. Defaults to True.",
                "default": True
            }
        },
        "required": ["path", "force"],
        "additionalProperties": False
    },
    "tool_function": clean_directory
} 