from typing import Callable, List, Dict, Any

import dotenv

import anthropic
from anthropic.types.message import Message

from tools.read_file import READ_FILE_DEFINITION
from tools.list_directory import LIST_DIRECTORY_DEFINITION

dotenv.load_dotenv()

class ToolDefinition:
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any], tool_function: Callable = None):
        self.name: str = name
        self.description: str = description
        self.input_schema: Dict[str, Any] = input_schema
        self.tool_function: Callable = tool_function

class Agent:
    def __init__(self, client: anthropic.Client, get_user_input: Callable[[], str], tools: List[ToolDefinition]):
        self.client: anthropic.Client = client
        self.get_user_input: Callable[[], str] = get_user_input
        self.tools: List[ToolDefinition] = tools

    def run(self):
        conversation: List[Dict[str, Any]] = []

        print("Chat with Claude (Ctrl-C to quit)")

        read_user_input = True
        while True:
            if read_user_input:
                print("You: ", end="", flush=True)
                try:
                    user_input = self.get_user_input()
                except Exception as e:
                    break
                
                user_message: Dict[str, Any] = {"role": "user", "content": user_input}
                conversation.append(user_message)
            
            message = self.run_inference(conversation)
            if message is None:
                break

            # Build assistant message content
            assistant_content = []
            tool_results = []
            
            for content in message.content:
                if content.type == "text":
                    assistant_content.append({
                        "type": "text",
                        "text": content.text
                    })
                    print(f"Claude: {content.text}")
                elif content.type == "tool_use":
                    assistant_content.append({
                        "type": "tool_use",
                        "id": content.id,
                        "name": content.name,
                        "input": content.input
                    })
                    result = self.execute_tool(content.id, content.name, content.input)
                    tool_results.append(result)
            
            # Add assistant message with all content (text and tool uses)
            if assistant_content:
                conversation.append({
                    "role": "assistant", 
                    "content": assistant_content
                })
            
            # Add tool results as part of the next user message
            if tool_results:
                # Create a user message with tool results
                user_content = []
                for result in tool_results:
                    user_content.append({
                        "type": "tool_result",
                        "tool_use_id": result["tool_use_id"],
                        "content": result["content"]
                    })
                
                conversation.append({
                    "role": "user",
                    "content": user_content
                })
            
            read_user_input = len(tool_results) == 0
    
            
    def run_inference(self, conversation: List[Dict[str, Any]]) -> Dict[str, Any]:
        tools = [anthropic.types.ToolParam(
                name=tool.name, description=tool.description, input_schema=tool.input_schema
            )
            for tool in self.tools]

        message: Message = self.client.messages.create(
            model="claude-3-7-sonnet-20250219",
            messages=conversation,
            max_tokens=1024,
            tools=tools,
        )
        return message

        
    def execute_tool(self, tool_id: str, tool_name: str, tool_input: Dict[str, Any]):
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if not tool:
            return {"tool_use_id": tool_id, "content": "tool not found", "is_error": True}
        
        try:
            response = tool.tool_function(**tool_input)
            return {"tool_use_id": tool_id, "content": response, "is_error": False}
        except Exception as e:
            return {"tool_use_id": tool_id, "content": str(e), "is_error": True}

class Tool:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
        self.name = name
        self.description = description
        self.parameters = parameters
        
def main():
    client = anthropic.Anthropic()
    tools: List[ToolDefinition] = [
        ToolDefinition(**READ_FILE_DEFINITION),
        ToolDefinition(**LIST_DIRECTORY_DEFINITION)
    ]
    agent = Agent(client, input, tools)
    agent.run()
       

if __name__ == "__main__":
    main()
