import asyncio
import json
import os
from typing import Optional, Dict, Any, List
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class ProperMCPClient:
    """Proper MCP client using the official MCP library with async support."""
    
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.available_tools = {}
        self.server_name = None
    
    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        self.available_tools = {tool.name: tool for tool in tools}
        self.server_name = server_script_path.split('/')[-1].split('.')[0]
        
        print(f"\nConnected to {self.server_name} server with tools: {list(self.available_tools.keys())}")
        return self.available_tools
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> str:
        """Call a tool on the MCP server."""
        if not self.session:
            raise Exception("Not connected to any MCP server")
        
        if tool_name not in self.available_tools:
            available_ops = list(self.available_tools.keys())
            raise ValueError(f"Tool '{tool_name}' not found. Available tools: {available_ops}")
        
        try:
            # Call the tool
            response = await self.session.call_tool(tool_name, arguments or {})
            
            # Return the content from the response
            if response.content:
                return response.content[0].text
            else:
                return "Operation completed successfully"
                
        except Exception as e:
            raise Exception(f"Error calling tool '{tool_name}': {str(e)}")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the connected server."""
        if not self.session:
            raise Exception("Not connected to any MCP server")
        
        response = await self.session.list_tools()
        tools = []
        for tool in response.tools:
            tool_info = {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            tools.append(tool_info)
        
        return tools
    
    async def close(self):
        """Close the MCP client connection."""
        if self.exit_stack:
            await self.exit_stack.aclose()

class MCPManager:
    """Manager for multiple MCP server connections."""
    
    def __init__(self):
        self.clients = {}
        self.exit_stack = AsyncExitStack()
    
    async def connect_to_filesystem_server(self):
        """Connect to the filesystem MCP server."""
        client = ProperMCPClient()
        await client.connect_to_server("npx @modelcontextprotocol/server-filesystem")
        self.clients["filesystem"] = client
        return client
    
    async def connect_to_git_server(self):
        """Connect to the git MCP server."""
        client = ProperMCPClient()
        await client.connect_to_server("npx @cyanheads/git-mcp-server")
        self.clients["git"] = client
        return client
    
    async def call_tool(self, server_type: str, tool_name: str, arguments: Dict[str, Any] = None) -> str:
        """Call a tool on a specific MCP server."""
        if server_type not in self.clients:
            if server_type == "filesystem":
                await self.connect_to_filesystem_server()
            elif server_type == "git":
                await self.connect_to_git_server()
            else:
                raise ValueError(f"Unknown server type: {server_type}")
        
        client = self.clients[server_type]
        return await client.call_tool(tool_name, arguments)
    
    async def list_tools(self, server_type: str) -> List[Dict[str, Any]]:
        """List available tools from a specific MCP server."""
        if server_type not in self.clients:
            if server_type == "filesystem":
                await self.connect_to_filesystem_server()
            elif server_type == "git":
                await self.connect_to_git_server()
            else:
                raise ValueError(f"Unknown server type: {server_type}")
        
        client = self.clients[server_type]
        return await client.list_tools()
    
    async def close_all(self):
        """Close all MCP client connections."""
        for client in self.clients.values():
            await client.close()
        await self.exit_stack.aclose()

# Global MCP manager instance
_mcp_manager = None

def get_mcp_manager() -> MCPManager:
    """Get the global MCP manager instance."""
    global _mcp_manager
    if _mcp_manager is None:
        _mcp_manager = MCPManager()
    return _mcp_manager

async def mcp_operation(server_type: str, tool_name: str, **kwargs) -> str:
    """Perform an MCP operation using the proper MCP client."""
    manager = get_mcp_manager()
    return await manager.call_tool(server_type, tool_name, kwargs)

async def list_mcp_tools(server_type: str) -> List[Dict[str, Any]]:
    """List available tools from an MCP server."""
    manager = get_mcp_manager()
    return await manager.list_tools(server_type) 