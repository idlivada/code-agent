import os
import time
from datetime import datetime

def get_file_info(path: str) -> str:
    """Get detailed information about a file or directory."""
    try:
        # Check if path exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path '{path}' not found")
        
        # Get basic stats
        stat = os.stat(path)
        
        # Determine if it's a file or directory
        is_file = os.path.isfile(path)
        is_dir = os.path.isdir(path)
        
        # Get file size
        size = stat.st_size
        size_str = f"{size} bytes"
        if size > 1024:
            size_str = f"{size / 1024:.1f} KB"
        if size > 1024 * 1024:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        
        # Get timestamps
        created_time = datetime.fromtimestamp(stat.st_ctime)
        modified_time = datetime.fromtimestamp(stat.st_mtime)
        accessed_time = datetime.fromtimestamp(stat.st_atime)
        
        # Get permissions
        permissions = oct(stat.st_mode)[-3:]
        
        # Build result
        result = [f"📄 File Information for: {path}"]
        result.append("=" * 50)
        
        if is_file:
            result.append(f"Type: File")
            result.append(f"Size: {size_str}")
        elif is_dir:
            result.append(f"Type: Directory")
            result.append(f"Size: {size_str}")
        
        result.append(f"Permissions: {permissions}")
        result.append(f"Created: {created_time.strftime('%Y-%m-%d %H:%M:%S')}")
        result.append(f"Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
        result.append(f"Accessed: {accessed_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Additional info for files
        if is_file:
            # Get file extension
            _, ext = os.path.splitext(path)
            if ext:
                result.append(f"Extension: {ext}")
            
            # Try to get line count for text files
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    result.append(f"Lines: {len(lines)}")
                    
                    # Count characters
                    content = ''.join(lines)
                    result.append(f"Characters: {len(content)}")
                    
            except (UnicodeDecodeError, PermissionError):
                result.append("Lines: Unable to read (binary file or permission denied)")
        
        # Additional info for directories
        elif is_dir:
            try:
                items = os.listdir(path)
                files = [item for item in items if os.path.isfile(os.path.join(path, item))]
                dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
                
                result.append(f"Files: {len(files)}")
                result.append(f"Directories: {len(dirs)}")
                result.append(f"Total items: {len(items)}")
                
            except PermissionError:
                result.append("Contents: Permission denied")
        
        return "\n".join(result)
        
    except Exception as e:
        raise Exception(f"Error getting file info for {path}: {str(e)}")

# Tool definition
GET_FILE_INFO_DEFINITION = {
    "name": "get_file_info",
    "description": "Get detailed information about a file or directory including size, timestamps, permissions, and more.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path of the file or directory to get information about."
            }
        },
        "required": ["path"],
        "additionalProperties": False
    },
    "tool_function": get_file_info
} 