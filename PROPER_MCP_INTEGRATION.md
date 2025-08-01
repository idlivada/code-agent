# Synchronous MCP Integration

This document describes the **synchronous** Model Context Protocol (MCP) integration for the AI-assisted code editor.

## 🎯 **Overview**

The MCP integration provides direct communication with external MCP servers for filesystem and Git operations, using **synchronous subprocess communication** instead of async/await patterns.

## 🏗️ **Architecture**

### **Core Components**

1. **`tools/sync_mcp_client.py`** - Synchronous MCP client using subprocess
2. **`tools/sync_mcp_wrapper.py`** - Tool definitions and wrappers
3. **`agent.py`** - Updated to use synchronous MCP tools

### **Key Features**

- ✅ **Synchronous Communication**: Direct subprocess-based JSON-RPC communication
- ✅ **No Async Dependencies**: Removed `asyncio` and `mcp` library dependencies
- ✅ **Simple Error Handling**: Straightforward exception handling
- ✅ **Process Management**: Automatic server process lifecycle management
- ✅ **Tool Discovery**: Dynamic tool discovery from MCP servers

## 🔧 **Available Tools**

### **Core Tools (9 total)**
1. `read_file` - Read file contents
2. `list_directory` - List directory contents
3. `edit_file` - Edit/create files with text replacement
4. `run_script` - Execute Python scripts
5. `run_tests` - Run Python tests (pytest/unittest)
6. `lint_code` - Lint and format code
7. `install_package` - Install Python packages
8. `generate_code` - Generate code snippets

### **MCP Tools (4 total)**
9. `sync_mcp_filesystem` - Filesystem operations via MCP
10. `sync_mcp_git` - Git operations via MCP
11. `sync_mcp_refresh_tools` - Refresh MCP tool caches
12. `sync_mcp_list_tools` - List available MCP tools

## 🚀 **How It Works**

### **1. Server Connection**
```python
# Direct subprocess communication
self.server_process = subprocess.Popen(
    server_command.split(),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)
```

### **2. JSON-RPC Communication**
```python
# Send request
request_str = json.dumps(request) + "\n"
self.server_process.stdin.write(request_str)
self.server_process.stdin.flush()

# Read response
response_line = self.server_process.stdout.readline()
response = json.loads(response_line.strip())
```

### **3. Tool Execution**
```python
# Synchronous tool call
result = sync_mcp_operation(server_type, tool_name, **kwargs)
return f"✅ MCP {server_type} {tool_name} completed successfully:\n{result}"
```

## 📦 **Dependencies**

### **Required Packages**
```txt
anthropic>=0.60.0
python-dotenv>=1.0.0
```

### **External Dependencies**
- **Node.js/npm**: For running MCP servers
- **Filesystem Server**: `npx @modelcontextprotocol/server-filesystem`
- **Git Server**: `npx @cyanheads/git-mcp-server`

## 🔄 **Tool Flow**

1. **User Request** → Agent receives request
2. **Tool Selection** → Agent chooses appropriate MCP tool
3. **Server Connection** → Synchronous connection to MCP server
4. **Tool Execution** → Direct JSON-RPC call to server
5. **Response Processing** → Parse and return results
6. **Result Display** → Show results to user

## 🛠️ **Benefits of Synchronous Approach**

- **Simpler Code**: No async/await complexity
- **Easier Debugging**: Straightforward error handling
- **Reduced Dependencies**: No external MCP library needed
- **Direct Control**: Full control over subprocess lifecycle
- **Immediate Results**: Synchronous execution flow

## 🔍 **Error Handling**

```python
try:
    result = sync_mcp_operation(server_type, tool_name, **kwargs)
    return f"✅ MCP {server_type} {tool_name} completed successfully:\n{result}"
except Exception as e:
    raise Exception(f"Error in MCP {server_type} operation '{tool_name}': {str(e)}")
```

## 📋 **Usage Examples**

### **Filesystem Operations**
```python
# List files in directory
sync_mcp_filesystem(tool_name="list_dir", path="/path/to/directory")

# Read file contents
sync_mcp_filesystem(tool_name="read_file", path="/path/to/file.txt")
```

### **Git Operations**
```python
# Check git status
sync_mcp_git(tool_name="status")

# Add files to staging
sync_mcp_git(tool_name="add", files=["file1.txt", "file2.py"])
```

### **Tool Discovery**
```python
# List available filesystem tools
sync_mcp_list_tools(server_type="filesystem")

# Refresh all MCP tool caches
sync_mcp_refresh_tools()
```

## 🎉 **Summary**

The synchronous MCP integration provides a **clean, simple, and efficient** way to interact with external MCP servers without the complexity of async programming. It maintains all the functionality while being easier to understand, debug, and maintain. 