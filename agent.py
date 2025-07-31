from typing import Callable, List, Dict, Any

import dotenv

import anthropic
from anthropic.types.message import Message

dotenv.load_dotenv()

class ToolDefinition:
    name: str
    description: str
    input_schema: Dict[str, Any]
    tool_function: Callable

class Agent:
    def __init__(self, client: anthropic.Client, get_user_input: Callable[[], str], tools: List[ToolDefinition]):
        self.client: anthropic.Client = client
        self.get_user_input: Callable[[], str] = get_user_input
        self.tools: List[ToolDefinition] = tools

    def run(self):
        conversation: List[Dict[str, str]] = []

        print("Chat with Claude (Ctrl-C to quit)")

        while True:
            print("You: ", end="", flush=True)
            try:
                user_input = self.get_user_input()
            except Exception as e:
                break

            user_message: Dict[str, str] = {"role": "user", "content": user_input}
            conversation.append(user_message)

            message = self.run_inference(conversation)
            if message is None:
                break

            conversation.append({"role": "assistant", "content": message.content[0].text})
            
            for content in message.content:
                if content.type == "text":
                    print(f"Claude: {content.text}")

    def run_inference(self, conversation: List[Dict[str, str]]) -> Dict[str, str]:
        tools = [anthropic.types.ToolParam(
                name=tool.name, description=tool.description, input_schema=tool.input_schema
            )
            for tool in self.tools]

        try:
            message: Message = self.client.messages.create(
                model="claude-3-7-sonnet-20250219",
                messages=conversation,
                max_tokens=1024,
                tools=tools,
            )
            return message
        except Exception as e:
            print(f"Inference error: {e}")
            return None


class Tool:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
        self.name = name
        self.description = description
        self.parameters = parameters
def main():
    client = anthropic.Anthropic()
    tools: List[ToolDefinition] = []
    agent = Agent(client, input, tools)
    agent.run()
       

if __name__ == "__main__":
    main()
