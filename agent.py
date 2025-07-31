from typing import Callable, List, Dict

import dotenv

import anthropic
from anthropic.types.message import Message

dotenv.load_dotenv()

class Agent:
    def __init__(self, client: anthropic.Client, get_user_input: Callable[[], str]):
        self.client: anthropic.Client = client
        self.get_user_input: Callable[[], str] = get_user_input

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
        try:
            message: Message = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                messages=conversation,
                max_tokens=1024
            )
            return message
        except Exception as e:
            print(f"Inference error: {e}")
            return None

def main():
    client = anthropic.Anthropic()
    agent = Agent(client, input)
    agent.run()
       

if __name__ == "__main__":
    main()
