# MCP Integration

This branch integrates Model Context Protocol (MCP) servers for enhanced file system and Git operations.

## MCP Servers Used

### 1. Filesystem Server
- **Source**: [Model Context Protocol Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- **Purpose**: Provides standardized file system operations
- **Operations**: read_file, write_file, delete_file, list_directory, create_directory, delete_directory, move_file, copy_file

### 2. Git Server
- **Source**: [Git MCP Server](https://github.com/cyanheads/git-mcp-server)
- **Purpose**: Provides comprehensive Git operations
- **Operations**: status, add, commit, diff, log, branch, checkout, pull, push, stash, clone, init, merge, rebase, reset, clean

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

### MCP Filesystem Tool (`mcp_filesystem`)
- **Operations**: read_file, write_file, delete_file, list_directory, create_directory, delete_directory, move_file, copy_file
- **Usage**: `mcp_filesystem(operation="read_file", path="file.txt")`

### MCP Git Tool (`mcp_git`)
- **Operations**: status, add, commit, diff, log, branch, checkout, pull, push, stash, clone, init, merge, rebase, reset, clean
- **Usage**: `mcp_git(operation="status")`

## Benefits of MCP Integration

1. **Standardization**: Uses industry-standard MCP protocol
2. **Extensibility**: Easy to add new MCP servers
3. **Separation of Concerns**: File/Git operations handled by specialized servers
4. **Better Error Handling**: MCP servers provide detailed error information
5. **Cross-Platform**: MCP servers work across different platforms

## Installation

To use the MCP servers, install the required packages:

```bash
npm install @modelcontextprotocol/server-filesystem @cyanheads/git-mcp-server
```

## Migration from Old Tools

The following tools have been replaced by MCP servers:

### Old File System Tools (Removed)
- `create_file` → `mcp_filesystem(operation="write_file")`
- `delete_file` → `mcp_filesystem(operation="delete_file")`
- `move_file` → `mcp_filesystem(operation="move_file")`
- `search_files` → Use `mcp_filesystem(operation="list_directory")` + `read_file`
- `get_file_info` → Use `mcp_filesystem(operation="read_file")` for content

### Old Directory Tools (Removed)
- `create_directory` → `mcp_filesystem(operation="create_directory")`
- `delete_directory` → `mcp_filesystem(operation="delete_directory")`
- `move_directory` → `mcp_filesystem(operation="move_file")` (for directories)
- `copy_directory` → `mcp_filesystem(operation="copy_file")` (for directories)
- `clean_directory` → Use `mcp_git(operation="clean")` for Git repositories

### Old Git Tools (Removed)
- `git_operations` → `mcp_git` (with enhanced operations)

## Current Tool Set

The agent now has **10 tools**:

1. `read_file` - Read file contents (legacy)
2. `list_directory` - Explore directory structure (legacy)
3. `edit_file` - Edit existing files (legacy)
4. `mcp_filesystem` - MCP filesystem operations
5. `mcp_git` - MCP git operations
6. `run_script` - Execute Python scripts
7. `run_tests` - Run test frameworks
8. `lint_code` - Code quality checks
9. `install_package` - Package management
10. `generate_code` - Code generation

## Future Enhancements

1. **Full MCP Integration**: Replace remaining legacy tools with MCP servers
2. **Additional MCP Servers**: Add servers for databases, APIs, etc.
3. **Enhanced Error Handling**: Better integration with MCP error reporting
4. **Configuration Management**: Dynamic MCP server configuration 