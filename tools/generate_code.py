import ast
import os
from typing import Dict, Any, List

def generate_code(description: str, language: str = "python", code_type: str = "function", filename: str = "") -> str:
    """Generate code snippets, functions, or classes based on descriptions."""
    try:
        # Validate parameters
        if not description:
            raise ValueError("Description cannot be empty")
        
        # This is a placeholder for code generation
        # In a real implementation, this would integrate with an LLM API
        # For now, we'll create a template based on the description
        
        if language.lower() == "python":
            if code_type.lower() == "function":
                # Generate a function template
                function_name = description.split()[0].lower() if description.split() else "generated_function"
                code = f'''def {function_name}():
    """
    {description}
    
    Returns:
        Any: The result of the function
    """
    # TODO: Implement the function based on description
    # {description}
    pass

# Example usage
if __name__ == "__main__":
    result = {function_name}()
    print(result)
'''
            elif code_type.lower() == "class":
                # Generate a class template
                class_name = description.split()[0].title() if description.split() else "GeneratedClass"
                code = f'''class {class_name}:
    """
    {description}
    """
    
    def __init__(self):
        """Initialize the {class_name}."""
        pass
    
    def process(self):
        """
        Main processing method.
        
        Returns:
            Any: The processed result
        """
        # TODO: Implement the processing logic
        # {description}
        pass

# Example usage
if __name__ == "__main__":
    instance = {class_name}()
    result = instance.process()
    print(result)
'''
            elif code_type.lower() == "script":
                # Generate a script template
                code = f'''#!/usr/bin/env python3
"""
{description}
"""

def main():
    """
    Main function to execute the script.
    """
    # TODO: Implement the main logic
    # {description}
    print("Script executed successfully")

if __name__ == "__main__":
    main()
'''
            else:
                raise ValueError(f"Unsupported code type: {code_type}")
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        # If filename is provided, save the code
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
                return f"✅ Generated {code_type} code and saved to {filename}:\n\n{code}"
            except Exception as e:
                return f"✅ Generated {code_type} code (failed to save to {filename}):\n\n{code}\n\nError: {str(e)}"
        else:
            return f"✅ Generated {code_type} code:\n\n{code}"
        
    except Exception as e:
        raise Exception(f"Error generating code: {str(e)}")

# Tool definition
GENERATE_CODE_DEFINITION = {
    "name": "generate_code",
    "description": "Generate code snippets, functions, or classes based on descriptions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Description of the code to generate."
            },
            "language": {
                "type": "string",
                "description": "Programming language for the generated code. Defaults to 'python'.",
                "default": "python"
            },
            "code_type": {
                "type": "string",
                "description": "Type of code to generate: 'function', 'class', or 'script'. Defaults to 'function'.",
                "default": "function"
            },
            "filename": {
                "type": "string",
                "description": "Optional filename to save the generated code.",
                "default": ""
            }
        },
        "required": ["description"],
        "additionalProperties": False
    },
    "tool_function": generate_code
} 