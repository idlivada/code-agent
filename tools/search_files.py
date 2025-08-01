import os
import re
from typing import List, Dict

def search_files(pattern: str, directory: str = ".", file_pattern: str = "*", case_sensitive: bool = False) -> str:
    """Search for text patterns across multiple files in a directory."""
    try:
        # Validate parameters
        if not pattern:
            raise ValueError("Search pattern cannot be empty")
        
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory '{directory}' not found")
        
        if not os.path.isdir(directory):
            raise ValueError(f"'{directory}' is not a directory")
        
        # Compile regex pattern
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)
        
        # Convert file_pattern to regex
        if file_pattern == "*":
            file_regex = re.compile(r".*")
        else:
            # Convert glob pattern to regex
            file_regex = re.compile(file_pattern.replace("*", ".*"))
        
        results = []
        total_files_searched = 0
        
        # Walk through directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                
                # Check if file matches pattern
                if not file_regex.match(file):
                    continue
                
                total_files_searched += 1
                
                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find matches
                    matches = list(regex.finditer(content))
                    
                    if matches:
                        file_result = {
                            "file": relative_path,
                            "matches": []
                        }
                        
                        for match in matches:
                            # Get line number
                            line_start = content.rfind('\n', 0, match.start()) + 1
                            line_end = content.find('\n', match.end())
                            if line_end == -1:
                                line_end = len(content)
                            
                            line_content = content[line_start:line_end].strip()
                            line_number = content[:match.start()].count('\n') + 1
                            
                            file_result["matches"].append({
                                "line": line_number,
                                "content": line_content,
                                "match": match.group()
                            })
                        
                        results.append(file_result)
                        
                except (UnicodeDecodeError, PermissionError):
                    # Skip binary files or files we can't read
                    continue
        
        # Format results
        if not results:
            return f"No matches found for pattern '{pattern}' in {total_files_searched} files"
        
        output = [f"Found {len(results)} files with matches for pattern '{pattern}':\n"]
        
        for result in results:
            output.append(f"📁 {result['file']}:")
            for match in result['matches']:
                output.append(f"  Line {match['line']}: {match['content']}")
            output.append("")
        
        output.append(f"Total files searched: {total_files_searched}")
        
        return "\n".join(output)
        
    except Exception as e:
        raise Exception(f"Error searching files: {str(e)}")

# Tool definition
SEARCH_FILES_DEFINITION = {
    "name": "search_files",
    "description": "Search for text patterns across multiple files in a directory.",
    "input_schema": {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "The regex pattern to search for."
            },
            "directory": {
                "type": "string",
                "description": "The directory to search in. Defaults to current directory.",
                "default": "."
            },
            "file_pattern": {
                "type": "string",
                "description": "File pattern to match (e.g., '*.py', '*.txt'). Defaults to all files.",
                "default": "*"
            },
            "case_sensitive": {
                "type": "boolean",
                "description": "Whether the search should be case sensitive. Defaults to False.",
                "default": False
            }
        },
        "required": ["pattern"],
        "additionalProperties": False
    },
    "tool_function": search_files
} 