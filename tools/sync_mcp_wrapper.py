import asyncio
import json
from typing import Dict, Any, List
from .proper_mcp_client import get_mcp_manager, mcp_operation, list_mcp_tools

def sync_mcp_operation(server_type: str, tool_name: str, **kwargs) -> str:
    """Synchronous wrapper for MCP operations."""
    try:
        # Run the async operation in an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(mcp_operation(server_type, tool_name, **kwargs))
            return f"✅ MCP {server_type} {tool_name} completed successfully:\n{result}"
        finally:
            loop.close()
    except Exception as e:
        raise Exception(f"Error in MCP {server_type} operation '{tool_name}': {str(e)}")

def sync_list_mcp_tools(server_type: str) -> str:
    """Synchronous wrapper for listing MCP tools."""
    try:
        # Run the async operation in an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            tools = loop.run_until_complete(list_mcp_tools(server_type))
            
            result = [f"🔧 Available {server_type} MCP tools ({len(tools)}):"]
            for tool in tools:
                result.append(f"  - {tool['name']}: {tool.get('description', 'No description')}")
                if 'inputSchema' in tool and 'properties' in tool['inputSchema']:
                    props = list(tool['inputSchema']['properties'].keys())
                    result.append(f"    Parameters: {', '.join(props)}")
                result.append("")
            
            return "\n".join(result)
        finally:
            loop.close()
    except Exception as e:
        raise Exception(f"Error listing MCP {server_type} tools: {str(e)}")

def sync_refresh_mcp_tools() -> str:
    """Synchronous wrapper for refreshing MCP tool caches."""
    try:
        # Run the async operation in an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = []
            
            # Refresh filesystem tools
            try:
                filesystem_tools = loop.run_until_complete(list_mcp_tools("filesystem"))
                results.append(f"📁 Filesystem tools discovered: {len(filesystem_tools)}")
                for tool in filesystem_tools:
                    results.append(f"  - {tool['name']}: {tool.get('description', 'No description')}")
            except Exception as e:
                results.append(f"❌ Filesystem tools discovery failed: {e}")
            
            # Refresh git tools
            try:
                git_tools = loop.run_until_complete(list_mcp_tools("git"))
                results.append(f"🔧 Git tools discovered: {len(git_tools)}")
                for tool in git_tools:
                    results.append(f"  - {tool['name']}: {tool.get('description', 'No description')}")
            except Exception as e:
                results.append(f"❌ Git tools discovery failed: {e}")
            
            return "\n".join(results)
        finally:
            loop.close()
    except Exception as e:
        raise Exception(f"Error refreshing MCP tools: {str(e)}")

# Tool definitions for the proper MCP integration
PROPER_MCP_FILESYSTEM_DEFINITION = {
    "name": "proper_mcp_filesystem",
    "description": "Perform filesystem operations using the proper MCP filesystem server with async support.",
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
    "tool_function": lambda **kwargs: sync_mcp_operation("filesystem", kwargs.pop("tool_name"), **kwargs)
}

PROPER_MCP_GIT_DEFINITION = {
    "name": "proper_mcp_git",
    "description": "Perform git operations using the proper MCP git server with async support.",
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
    "tool_function": lambda **kwargs: sync_mcp_operation("git", kwargs.pop("tool_name"), **kwargs)
}

PROPER_MCP_REFRESH_TOOLS_DEFINITION = {
    "name": "proper_mcp_refresh_tools",
    "description": "Refresh MCP tool caches using the proper MCP client.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    },
    "tool_function": sync_refresh_mcp_tools
}

PROPER_MCP_LIST_TOOLS_DEFINITION = {
    "name": "proper_mcp_list_tools",
    "description": "List available MCP tools using the proper MCP client.",
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
    "tool_function": lambda server_type="filesystem": sync_list_mcp_tools(server_type)
} 