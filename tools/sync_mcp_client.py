import json
import subprocess
import os
from typing import Optional, Dict, Any, List

class SyncMCPClient:
    """Synchronous MCP client using subprocess for direct communication."""
    
    def __init__(self):
        self.server_process = None
        self.available_tools = {}
        self.server_name = None
        self.request_id = 0
    
    def connect_to_server(self, server_command: str):
        """Connect to an MCP server using subprocess

        Args:
            server_command: Command to start the MCP server (e.g., "npx @modelcontextprotocol/server-filesystem")
        """
        try:
            # Start the server process
            self.server_process = subprocess.Popen(
                server_command.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Initialize the session
            init_request = {
                "jsonrpc": "2.0",
                "id": self._get_next_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "sync-mcp-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = self._send_request(init_request)
            if "error" in response:
                raise Exception(f"Failed to initialize MCP server: {response['error']}")
            
            # List available tools
            tools_response = self.list_tools()
            self.server_name = server_command.split()[-1].split('/')[-1]
            
            print(f"\nConnected to {self.server_name} server with tools: {list(self.available_tools.keys())}")
            return self.available_tools
            
        except Exception as e:
            if self.server_process:
                self.server_process.terminate()
            raise Exception(f"Failed to connect to MCP server: {str(e)}")
    
    def _get_next_id(self) -> int:
        """Get the next request ID."""
        self.request_id += 1
        return self.request_id
    
    def _send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server."""
        if not self.server_process:
            raise Exception("Not connected to any MCP server")
        
        try:
            # Send the request
            request_str = json.dumps(request) + "\n"
            self.server_process.stdin.write(request_str)
            self.server_process.stdin.flush()
            
            # Read the response
            response_line = self.server_process.stdout.readline()
            if not response_line:
                raise Exception("No response from MCP server")
            
            response = json.loads(response_line.strip())
            return response
            
        except Exception as e:
            raise Exception(f"Error communicating with MCP server: {str(e)}")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> str:
        """Call a tool on the MCP server."""
        if tool_name not in self.available_tools:
            available_ops = list(self.available_tools.keys())
            raise ValueError(f"Tool '{tool_name}' not found. Available tools: {available_ops}")
        
        try:
            # Call the tool
            request = {
                "jsonrpc": "2.0",
                "id": self._get_next_id(),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments or {}
                }
            }
            
            response = self._send_request(request)
            
            if "error" in response:
                raise Exception(f"Tool call failed: {response['error']}")
            
            # Extract content from response
            if "result" in response and "content" in response["result"]:
                content = response["result"]["content"]
                if content and len(content) > 0:
                    return content[0].get("text", "Operation completed successfully")
            
            return "Operation completed successfully"
                
        except Exception as e:
            raise Exception(f"Error calling tool '{tool_name}': {str(e)}")
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the connected server."""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._get_next_id(),
                "method": "tools/list",
                "params": {}
            }
            
            response = self._send_request(request)
            
            if "error" in response:
                raise Exception(f"Failed to list tools: {response['error']}")
            
            tools = []
            if "result" in response and "tools" in response["result"]:
                for tool in response["result"]["tools"]:
                    tool_info = {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "inputSchema": tool.get("inputSchema", {})
                    }
                    tools.append(tool_info)
                    self.available_tools[tool["name"]] = tool_info
            
            return tools
            
        except Exception as e:
            raise Exception(f"Error listing tools: {str(e)}")
    
    def close(self):
        """Close the MCP client connection."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

class SyncMCPManager:
    """Manager for multiple synchronous MCP server connections."""
    
    def __init__(self):
        self.clients = {}
    
    def connect_to_filesystem_server(self):
        """Connect to the filesystem MCP server."""
        client = SyncMCPClient()
        client.connect_to_server("npx @modelcontextprotocol/server-filesystem")
        self.clients["filesystem"] = client
        return client
    
    def connect_to_git_server(self):
        """Connect to the git MCP server."""
        client = SyncMCPClient()
        client.connect_to_server("npx @cyanheads/git-mcp-server")
        self.clients["git"] = client
        return client
    
    def call_tool(self, server_type: str, tool_name: str, arguments: Dict[str, Any] = None) -> str:
        """Call a tool on a specific MCP server."""
        if server_type not in self.clients:
            if server_type == "filesystem":
                self.connect_to_filesystem_server()
            elif server_type == "git":
                self.connect_to_git_server()
            else:
                raise ValueError(f"Unknown server type: {server_type}")
        
        client = self.clients[server_type]
        return client.call_tool(tool_name, arguments)
    
    def list_tools(self, server_type: str) -> List[Dict[str, Any]]:
        """List available tools from a specific MCP server."""
        if server_type not in self.clients:
            if server_type == "filesystem":
                self.connect_to_filesystem_server()
            elif server_type == "git":
                self.connect_to_git_server()
            else:
                raise ValueError(f"Unknown server type: {server_type}")
        
        client = self.clients[server_type]
        return client.list_tools()
    
    def close_all(self):
        """Close all MCP client connections."""
        for client in self.clients.values():
            client.close()

# Global MCP manager instance
_sync_mcp_manager = None

def get_sync_mcp_manager() -> SyncMCPManager:
    """Get the global synchronous MCP manager instance."""
    global _sync_mcp_manager
    if _sync_mcp_manager is None:
        _sync_mcp_manager = SyncMCPManager()
    return _sync_mcp_manager

def sync_mcp_operation(server_type: str, tool_name: str, **kwargs) -> str:
    """Perform an MCP operation using the synchronous MCP client."""
    manager = get_sync_mcp_manager()
    return manager.call_tool(server_type, tool_name, kwargs)

def sync_list_mcp_tools(server_type: str) -> List[Dict[str, Any]]:
    """List available tools from an MCP server."""
    manager = get_sync_mcp_manager()
    return manager.list_tools(server_type) 