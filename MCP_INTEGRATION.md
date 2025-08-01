# Dynamic MCP Integration

This branch integrates Model Context Protocol (MCP) servers with **dynamic operation discovery** for enhanced file system and Git operations.

## 🚀 Dynamic MCP Servers

### 1. Filesystem Server
- **Source**: [Model Context Protocol Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- **Purpose**: Provides standardized file system operations
- **Dynamic Operations**: Automatically discovers all available operations

### 2. Git Server
- **Source**: [Git MCP Server](https://github.com/cyanheads/git-mcp-server)
- **Purpose**: Provides comprehensive Git operations
- **Dynamic Operations**: Automatically discovers all available operations

## 🔄 Dynamic Operation Discovery

The key innovation is **automatic operation discovery**. Instead of hardcoding operations, the system:

1. **Discovers available tools** from MCP servers at runtime
2. **Dynamically generates tool schemas** based on server capabilities
3. **Automatically adapts** to new operations added to MCP servers
4. **No code changes required** when servers add new operations

## Configuration

The MCP servers are configured in `mcp_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem"],
      "env": {
        "MCP_LOG_LEVEL": "info"
      }
    },
    "git": {
      "command": "npx",
      "args": ["@cyanheads/git-mcp-server"],
      "env": {
        "MCP_LOG_LEVEL": "info",
        "GIT_SIGN_COMMITS": "false"
      }
    }
  }
}
```

## Available Tools

### Dynamic MCP Tools (2 tools):
1. **`dynamic_mcp_filesystem`** - Dynamic filesystem operations
   - **Auto-discovers** all available filesystem operations
   - **No code changes** when new operations are added
   - **Usage**: `dynamic_mcp_filesystem(operation="read_file", path="file.txt")`

2. **`dynamic_mcp_git`** - Dynamic git operations
   - **Auto-discovers** all available git operations
   - **No code changes** when new operations are added
   - **Usage**: `dynamic_mcp_git(operation="status")`

### MCP Management Tools (3 tools):
3. **`mcp_refresh_tools`** - Refresh tool caches
   - Discovers new operations from MCP servers
   - Updates available operation lists

4. **`mcp_list_operations`** - List available operations
   - Shows all operations from filesystem and git servers
   - Includes parameter information

5. **`mcp_operation_info`** - Get operation details
   - Detailed information about specific operations
   - Parameter descriptions and requirements

## Benefits of Dynamic Integration

1. **Zero Maintenance**: No code changes when MCP servers add operations
2. **Automatic Discovery**: New operations are automatically available
3. **Schema Validation**: Dynamic parameter validation based on server schemas
4. **Future-Proof**: Works with any MCP server updates
5. **Extensible**: Easy to add new MCP servers

## Installation

To use the MCP servers, install the required packages:

```bash
npm install @modelcontextprotocol/server-filesystem @cyanheads/git-mcp-server
```

## Usage Examples

### Discovering Operations
```
"List all available MCP operations"
"Refresh MCP tool caches to discover new operations"
"Get detailed information about the git status operation"
```

### Using Dynamic Operations
```
"Use dynamic filesystem to read a file"
"Use dynamic git to check repository status"
"Use dynamic filesystem to create a new directory"
```

## Current Tool Set (13 tools)

### Legacy Tools (3 tools):
1. `read_file` - Read file contents (legacy)
2. `list_directory` - Explore directory structure (legacy)
3. `edit_file` - Edit existing files (legacy)

### Dynamic MCP Tools (2 tools):
4. `dynamic_mcp_filesystem` - **Dynamic filesystem operations**
5. `dynamic_mcp_git` - **Dynamic git operations**

### MCP Management Tools (3 tools):
6. `mcp_refresh_tools` - Refresh MCP tool caches
7. `mcp_list_operations` - List available operations
8. `mcp_operation_info` - Get operation details

### Execution & Development Tools (5 tools):
9. `run_script` - Execute Python scripts
10. `run_tests` - Run test frameworks
11. `lint_code` - Code quality checks
12. `install_package` - Package management
13. `generate_code` - Code generation

## How Dynamic Discovery Works

1. **Tool Discovery**: MCP client calls `tools/list` on server startup
2. **Schema Generation**: Tool schemas are generated from server responses
3. **Dynamic Validation**: Parameters are validated against server schemas
4. **Runtime Execution**: Operations are executed through MCP protocol
5. **Cache Management**: Tool caches can be refreshed to discover new operations

## Future Enhancements

1. **Auto-Refresh**: Automatically refresh tool caches when servers update
2. **Server Health Monitoring**: Monitor MCP server availability
3. **Performance Optimization**: Cache tool schemas for better performance
4. **Additional MCP Servers**: Easy integration of new MCP servers
5. **Advanced Validation**: Enhanced parameter validation and error handling

## Migration from Static Tools

The dynamic approach eliminates the need for:
- Manual operation mapping
- Code updates for new operations
- Static tool definitions
- Hardcoded parameter validation

**Result**: A truly dynamic and maintainable MCP integration! 