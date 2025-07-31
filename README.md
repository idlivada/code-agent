# Code Agent

A simple chat interface for interacting with Claude AI using the Anthropic API.

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd code-agent
```

2. Create a virtual environment:
```bash
python -m venv coding-agent-env
source coding-agent-env/bin/activate  # On Windows: coding-agent-env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the agent:
```bash
python agent.py
```

The agent will start a chat session with Claude. Type your messages and press Enter to send them. Use Ctrl-C to quit.

## Features

- Interactive chat interface with Claude AI
- Conversation history maintained during session
- Environment variable configuration for API keys
- Simple and clean command-line interface

## Requirements

- Python 3.7+
- Anthropic API key
- Internet connection for API calls 