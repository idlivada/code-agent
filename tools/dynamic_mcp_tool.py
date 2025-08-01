import json
import os
from typing import Dict, Any, Optional
from .dynamic_mcp_client import create_dynamic_filesystem_client, create_dynamic_git_client

# Global cache for discovered tools
_filesystem_tools_cache = None
_git_tools_cache = None

def get_filesystem_tools() -> Dict[str, Any]:
    """Get available filesystem tools from MCP server."""
    global _filesystem_tools_cache
    
    if _filesystem_tools_cache is None:
        try:
            client = create_dynamic_filesystem_client()
            tools = client.discover_tools()
            _filesystem_tools_cache = {tool["name"]: tool for tool in tools}
        except Exception as e:
            print(f"Warning: Could not discover filesystem tools: {e}")
            _filesystem_tools_cache = {}
    
    return _filesystem_tools_cache

def get_git_tools() -> Dict[str, Any]:
    """Get available git tools from MCP server."""
    global _git_tools_cache
    
    if _git_tools_cache is None:
        try:
            client = create_dynamic_git_client()
            tools = client.discover_tools()
            _git_tools_cache = {tool["name"]: tool for tool in tools}
        except Exception as e:
            print(f"Warning: Could not discover git tools: {e}")
            _git_tools_cache = {}
    
    return _git_tools_cache

def dynamic_mcp_operation(server_type: str, operation: str, **kwargs) -> str:
    """Perform dynamic MCP operations that automatically discover available tools."""
    try:
        # Validate parameters
        if not server_type:
            raise ValueError("Server type cannot be empty")
        if not operation:
            raise ValueError("Operation cannot be empty")
        
        # Get available tools based on server type
        if server_type.lower() == "filesystem":
            available_tools = get_filesystem_tools()
            client = create_dynamic_filesystem_client()
        elif server_type.lower() == "git":
            available_tools = get_git_tools()
            client = create_dynamic_git_client()
        else:
            raise ValueError(f"Unsupported server type: {server_type}")
        
        # Check if operation is available
        if operation not in available_tools:
            available_ops = list(available_tools.keys())
            raise ValueError(f"Operation '{operation}' not found. Available operations: {available_ops}")
        
        # Get tool schema for validation
        tool_schema = available_tools[operation]
        
        # Validate arguments against schema if available
        if "inputSchema" in tool_schema:
            schema = tool_schema["inputSchema"]
            if "properties" in schema:
                required_props = schema.get("required", [])
                
                # Check for required properties
                for prop in required_props:
                    if prop not in kwargs:
                        raise ValueError(f"Required argument '{prop}' missing for operation '{operation}'")
                
                # Check for unknown properties
                allowed_props = list(schema["properties"].keys())
                for key in kwargs:
                    if key not in allowed_props:
                        print(f"Warning: Unknown argument '{key}' for operation '{operation}'")
        
        # Call the MCP server
        result = client.call_tool(operation, kwargs)
        return f"✅ Dynamic MCP {server_type} {operation} completed successfully:\n{result}"
        
    except Exception as e:
        raise Exception(f"Error in dynamic MCP {server_type} operation '{operation}': {str(e)}")

def get_dynamic_mcp_tool_definition(server_type: str) -> Dict[str, Any]:
    """Generate a dynamic tool definition for the specified MCP server type."""
    
    if server_type.lower() == "filesystem":
        available_tools = get_filesystem_tools()
        description = "Dynamic filesystem operations using MCP filesystem server"
    elif server_type.lower() == "git":
        available_tools = get_git_tools()
        description = "Dynamic git operations using MCP git server"
    else:
        raise ValueError(f"Unsupported server type: {server_type}")
    
    # Generate properties from available tools
    properties = {
        "server_type": {
            "type": "string",
            "description": f"The MCP server type: '{server_type}'",
            "default": server_type
        },
        "operation": {
            "type": "string",
            "description": f"The operation to perform. Available operations: {list(available_tools.keys())}"
        }
    }
    
    # Add dynamic properties based on available tools
    for tool_name, tool_info in available_tools.items():
        if "inputSchema" in tool_info and "properties" in tool_info["inputSchema"]:
            schema_props = tool_info["inputSchema"]["properties"]
            for prop_name, prop_info in schema_props.items():
                if prop_name not in properties:
                    properties[prop_name] = {
                        "type": prop_info.get("type", "string"),
                        "description": f"Argument for {tool_name}: {prop_info.get('description', 'No description')}"
                    }
    
    return {
        "name": f"dynamic_mcp_{server_type}",
        "description": f"{description}. Automatically discovers and uses any operations available from the MCP server.",
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": ["operation"],
            "additionalProperties": True
        },
        "tool_function": lambda **kwargs: dynamic_mcp_operation(server_type, **kwargs)
    }

# Generate tool definitions
DYNAMIC_MCP_FILESYSTEM_DEFINITION = get_dynamic_mcp_tool_definition("filesystem")
DYNAMIC_MCP_GIT_DEFINITION = get_dynamic_mcp_tool_definition("git") 