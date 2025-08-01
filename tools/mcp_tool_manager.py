import json
from typing import Dict, Any, List
from .dynamic_mcp_client import create_dynamic_filesystem_client, create_dynamic_git_client

def refresh_mcp_tools() -> str:
    """Refresh the MCP tool caches to discover new operations."""
    try:
        results = []
        
        # Refresh filesystem tools
        try:
            client = create_dynamic_filesystem_client()
            filesystem_tools = client.discover_tools()
            results.append(f"📁 Filesystem tools discovered: {len(filesystem_tools)}")
            for tool in filesystem_tools:
                results.append(f"  - {tool['name']}: {tool.get('description', 'No description')}")
        except Exception as e:
            results.append(f"❌ Filesystem tools discovery failed: {e}")
        
        # Refresh git tools
        try:
            client = create_dynamic_git_client()
            git_tools = client.discover_tools()
            results.append(f"🔧 Git tools discovered: {len(git_tools)}")
            for tool in git_tools:
                results.append(f"  - {tool['name']}: {tool.get('description', 'No description')}")
        except Exception as e:
            results.append(f"❌ Git tools discovery failed: {e}")
        
        return "\n".join(results)
        
    except Exception as e:
        raise Exception(f"Error refreshing MCP tools: {str(e)}")

def list_mcp_operations(server_type: str = "all") -> str:
    """List available MCP operations for the specified server type."""
    try:
        results = []
        
        if server_type.lower() in ["all", "filesystem"]:
            try:
                client = create_dynamic_filesystem_client()
                filesystem_tools = client.discover_tools()
                results.append(f"📁 Filesystem Operations ({len(filesystem_tools)}):")
                for tool in filesystem_tools:
                    results.append(f"  - {tool['name']}")
                    if "inputSchema" in tool and "properties" in tool["inputSchema"]:
                        props = list(tool["inputSchema"]["properties"].keys())
                        results.append(f"    Parameters: {', '.join(props)}")
                    results.append("")
            except Exception as e:
                results.append(f"❌ Filesystem operations discovery failed: {e}")
        
        if server_type.lower() in ["all", "git"]:
            try:
                client = create_dynamic_git_client()
                git_tools = client.discover_tools()
                results.append(f"🔧 Git Operations ({len(git_tools)}):")
                for tool in git_tools:
                    results.append(f"  - {tool['name']}")
                    if "inputSchema" in tool and "properties" in tool["inputSchema"]:
                        props = list(tool["inputSchema"]["properties"].keys())
                        results.append(f"    Parameters: {', '.join(props)}")
                    results.append("")
            except Exception as e:
                results.append(f"❌ Git operations discovery failed: {e}")
        
        return "\n".join(results)
        
    except Exception as e:
        raise Exception(f"Error listing MCP operations: {str(e)}")

def get_mcp_operation_info(server_type: str, operation: str) -> str:
    """Get detailed information about a specific MCP operation."""
    try:
        if server_type.lower() == "filesystem":
            client = create_dynamic_filesystem_client()
        elif server_type.lower() == "git":
            client = create_dynamic_git_client()
        else:
            raise ValueError(f"Unsupported server type: {server_type}")
        
        tools = client.discover_tools()
        tool_info = None
        
        for tool in tools:
            if tool["name"] == operation:
                tool_info = tool
                break
        
        if not tool_info:
            available_ops = [tool["name"] for tool in tools]
            raise ValueError(f"Operation '{operation}' not found. Available operations: {available_ops}")
        
        # Format tool information
        result = [f"🔍 MCP {server_type} Operation: {operation}"]
        result.append("=" * 50)
        
        if "description" in tool_info:
            result.append(f"Description: {tool_info['description']}")
        
        if "inputSchema" in tool_info:
            schema = tool_info["inputSchema"]
            result.append(f"Input Schema:")
            
            if "properties" in schema:
                for prop_name, prop_info in schema["properties"].items():
                    result.append(f"  - {prop_name}: {prop_info.get('type', 'unknown')}")
                    if "description" in prop_info:
                        result.append(f"    Description: {prop_info['description']}")
                    if "required" in schema and prop_name in schema["required"]:
                        result.append(f"    Required: Yes")
                    else:
                        result.append(f"    Required: No")
                    result.append("")
        
        return "\n".join(result)
        
    except Exception as e:
        raise Exception(f"Error getting MCP operation info: {str(e)}")

# Tool definitions for MCP management
MCP_REFRESH_TOOLS_DEFINITION = {
    "name": "mcp_refresh_tools",
    "description": "Refresh MCP tool caches to discover new operations from MCP servers.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    },
    "tool_function": refresh_mcp_tools
}

MCP_LIST_OPERATIONS_DEFINITION = {
    "name": "mcp_list_operations",
    "description": "List available MCP operations for filesystem and git servers.",
    "input_schema": {
        "type": "object",
        "properties": {
            "server_type": {
                "type": "string",
                "description": "Server type to list operations for: 'all', 'filesystem', or 'git'.",
                "default": "all"
            }
        },
        "required": [],
        "additionalProperties": False
    },
    "tool_function": list_mcp_operations
}

MCP_OPERATION_INFO_DEFINITION = {
    "name": "mcp_operation_info",
    "description": "Get detailed information about a specific MCP operation.",
    "input_schema": {
        "type": "object",
        "properties": {
            "server_type": {
                "type": "string",
                "description": "The MCP server type: 'filesystem' or 'git'."
            },
            "operation": {
                "type": "string",
                "description": "The operation name to get information about."
            }
        },
        "required": ["server_type", "operation"],
        "additionalProperties": False
    },
    "tool_function": get_mcp_operation_info
} 