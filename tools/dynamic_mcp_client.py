import subprocess
import json
import os
from typing import Dict, Any, Optional, List

class DynamicMCPClient:
    """Dynamic client for communicating with MCP servers that can discover available operations."""
    
    def __init__(self, server_command: list, env_vars: Dict[str, str] = None):
        self.server_command = server_command
        self.env_vars = env_vars or {}
        self.process = None
        self.available_tools = None
    
    def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools from the MCP server."""
        try:
            # Create the tools/list request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            # Start the MCP server process
            self.process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=self.env_vars
            )
            
            # Send the request
            request_json = json.dumps(request) + "\n"
            stdout, stderr = self.process.communicate(input=request_json, timeout=30)
            
            # Parse the response
            try:
                response = json.loads(stdout.strip())
                
                if "error" in response:
                    error_msg = response["error"].get("message", "Unknown MCP error")
                    raise Exception(f"MCP server error: {error_msg}")
                
                if "result" in response and "tools" in response["result"]:
                    self.available_tools = response["result"]["tools"]
                    return self.available_tools
                else:
                    return []
                    
            except json.JSONDecodeError:
                return []
            
        except subprocess.TimeoutExpired:
            if self.process:
                self.process.kill()
            raise Exception(f"MCP tool discovery timed out after 30 seconds")
        except FileNotFoundError:
            raise Exception(f"MCP server not found. Please install the required package.")
        except Exception as e:
            raise Exception(f"Error discovering MCP tools: {str(e)}")
        finally:
            if self.process:
                self.process.terminate()
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> str:
        """Call a tool on the MCP server."""
        try:
            # Create the MCP request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments or {}
                }
            }
            
            # Start the MCP server process
            self.process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=self.env_vars
            )
            
            # Send the request
            request_json = json.dumps(request) + "\n"
            stdout, stderr = self.process.communicate(input=request_json, timeout=60)
            
            # Parse the response
            try:
                response = json.loads(stdout.strip())
                
                if "error" in response:
                    error_msg = response["error"].get("message", "Unknown MCP error")
                    raise Exception(f"MCP server error: {error_msg}")
                
                if "result" in response:
                    result = response["result"]
                    if "content" in result:
                        return result['content']
                    else:
                        return "Operation completed successfully"
                else:
                    return "Operation completed successfully"
                    
            except json.JSONDecodeError:
                # If response is not JSON, it might be a direct output
                if stdout.strip():
                    return stdout.strip()
                else:
                    return "Operation completed successfully"
            
        except subprocess.TimeoutExpired:
            if self.process:
                self.process.kill()
            raise Exception(f"MCP operation timed out after 60 seconds")
        except FileNotFoundError:
            raise Exception(f"MCP server not found. Please install the required package.")
        except Exception as e:
            raise Exception(f"Error in MCP operation: {str(e)}")
        finally:
            if self.process:
                self.process.terminate()

def create_dynamic_filesystem_client() -> DynamicMCPClient:
    """Create a dynamic MCP client for filesystem operations."""
    return DynamicMCPClient(
        ["npx", "@modelcontextprotocol/server-filesystem"],
        {"MCP_LOG_LEVEL": "info"}
    )

def create_dynamic_git_client() -> DynamicMCPClient:
    """Create a dynamic MCP client for git operations."""
    return DynamicMCPClient(
        ["npx", "@cyanheads/git-mcp-server"],
        {"MCP_LOG_LEVEL": "info", "GIT_SIGN_COMMITS": "false"}
    ) 