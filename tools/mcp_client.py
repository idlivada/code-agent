import subprocess
import json
import os
from typing import Dict, Any, Optional

class MCPClient:
    """Client for communicating with MCP servers."""
    
    def __init__(self, server_command: list, env_vars: Dict[str, str] = None):
        self.server_command = server_command
        self.env_vars = env_vars or {}
        self.process = None
    
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

def create_filesystem_client() -> MCPClient:
    """Create an MCP client for filesystem operations."""
    return MCPClient(
        ["npx", "@modelcontextprotocol/server-filesystem"],
        {"MCP_LOG_LEVEL": "info"}
    )

def create_git_client() -> MCPClient:
    """Create an MCP client for git operations."""
    return MCPClient(
        ["npx", "@cyanheads/git-mcp-server"],
        {"MCP_LOG_LEVEL": "info", "GIT_SIGN_COMMITS": "false"}
    ) 