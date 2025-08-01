import json
from typing import Dict, Any, List
from .sync_mcp_client import get_sync_mcp_manager, sync_mcp_operation, sync_list_mcp_tools

def sync_mcp_operation_wrapper(server_type: str, tool_name: str, **kwargs) -> str:
    """Synchronous wrapper for MCP operations."""
    try:
        result = sync_mcp_operation(server_type, tool_name, **kwargs)
        return f"✅ MCP {server_type} {tool_name} completed successfully:\n{result}"
    except Exception as e:
        raise Exception(f"Error in MCP {server_type} operation '{tool_name}': {str(e)}")

def sync_list_mcp_tools_wrapper(server_type: str) -> str:
    """Synchronous wrapper for listing MCP tools."""
    try:
        tools = sync_list_mcp_tools(server_type)
        
        result = [f"🔧 Available {server_type} MCP tools ({len(tools)}):"]
        for tool in tools:
            result.append(f"  - {tool['name']}: {tool.get('description', 'No description')}")
            if 'inputSchema' in tool and 'properties' in tool['inputSchema']:
                props = list(tool['inputSchema']['properties'].keys())
                result.append(f"    Parameters: {', '.join(props)}")
            result.append("")
        
        return "\n".join(result)
    except Exception as e:
        raise Exception(f"Error listing MCP {server_type} tools: {str(e)}")

def sync_refresh_mcp_tools_wrapper() -> str:
    """Synchronous wrapper for refreshing MCP tool caches."""
    try:
        results = []
        
        # Refresh filesystem tools
        try:
            filesystem_tools = sync_list_mcp_tools("filesystem")
            results.append(f"📁 Filesystem tools discovered: {len(filesystem_tools)}")
            for tool in filesystem_tools:
                results.append(f"  - {tool['name']}: {tool.get('description', 'No description')}")
        except Exception as e:
            results.append(f"❌ Filesystem tools discovery failed: {e}")
        
        # Refresh git tools
        try:
            git_tools = sync_list_mcp_tools("git")
            results.append(f"🔧 Git tools discovered: {len(git_tools)}")
            for tool in git_tools:
                results.append(f"  - {tool['name']}: {tool.get('description', 'No description')}")
        except Exception as e:
            results.append(f"❌ Git tools discovery failed: {e}")
        
        return "\n".join(results)
    except Exception as e:
        raise Exception(f"Error refreshing MCP tools: {str(e)}")

# Tool definitions for the synchronous MCP integration
SYNC_MCP_FILESYSTEM_DEFINITION = {
    "name": "sync_mcp_filesystem",
    "description": "Perform filesystem operations using the synchronous MCP filesystem server.",
    "input_schema": {
        "type": "object",
        "properties": {
            "tool_name": {
                "type": "string",
                "description": "The filesystem operation to perform (discovered automatically from server)."
            },
            "server_type": {
                "type": "string",
                "description": "The MCP server type (defaults to 'filesystem').",
                "default": "filesystem"
            }
        },
        "required": ["tool_name"],
        "additionalProperties": True
    },
    "tool_function": lambda **kwargs: sync_mcp_operation_wrapper("filesystem", kwargs.pop("tool_name"), **kwargs)
}

SYNC_MCP_GIT_DEFINITION = {
    "name": "sync_mcp_git",
    "description": "Perform git operations using the synchronous MCP git server.",
    "input_schema": {
        "type": "object",
        "properties": {
            "tool_name": {
                "type": "string",
                "description": "The git operation to perform (discovered automatically from server)."
            },
            "server_type": {
                "type": "string",
                "description": "The MCP server type (defaults to 'git').",
                "default": "git"
            }
        },
        "required": ["tool_name"],
        "additionalProperties": True
    },
    "tool_function": lambda **kwargs: sync_mcp_operation_wrapper("git", kwargs.pop("tool_name"), **kwargs)
}

SYNC_MCP_REFRESH_TOOLS_DEFINITION = {
    "name": "sync_mcp_refresh_tools",
    "description": "Refresh MCP tool caches using the synchronous MCP client.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    },
    "tool_function": sync_refresh_mcp_tools_wrapper
}

SYNC_MCP_LIST_TOOLS_DEFINITION = {
    "name": "sync_mcp_list_tools",
    "description": "List available MCP tools using the synchronous MCP client.",
    "input_schema": {
        "type": "object",
        "properties": {
            "server_type": {
                "type": "string",
                "description": "Server type to list tools for: 'filesystem' or 'git'.",
                "default": "filesystem"
            }
        },
        "required": [],
        "additionalProperties": False
    },
    "tool_function": lambda server_type="filesystem": sync_list_mcp_tools_wrapper(server_type)
} 