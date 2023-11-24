
# GPT-RAG Orchestrator App README

## Overview
This application is an interactive chat application that utilizes an Azure Function-based orchestrator to connect with the GPT-RAG model [gpt-rag-orchestrator](https://github.com/Azure/gpt-rag-orchestrator/tree/147e1cb8545eae368580f6eaa182a56f4f7610a9). The app provides a user interface with TK for sending queries and receiving responses from the model. 

<img src="media/chat.PNG" alt="Chat preview" width="512">

## Files
- `main.py`: The entry point for the application. It initializes and runs the chat application.
- `chat.py`: Contains the `Chat` class, which sets up the GUI for the chat application using Tkinter and handles the interaction logic.
- `env.template`: A template for setting up environment variables required for the application, such as API keys and endpoint URLs.
- `orchestrator_request.py`: Handles the communication with the orchestrator Azure Function, sending requests and receiving responses from the GPT-RAG model.

## Prerequisites
- Python 3.x
- `tkinter`, `requests`, `flask`, `flask_cors`, `dotenv`, `azure-identity`, and `azure-keyvault-secrets` libraries.
- An Azure account with a deployed orchestrator function.
- OpenAI API key.


# Getting Started

# WINDOWS
1. Create a Virtual Environment (`python3 -m venv /path/to/new/virtual/environment`)
2. Activate Virtual Environment (`path\to\venv\Scripts\activate.bat`)
3. Install requirements.txt (`pip install -r requirements.txt`)


## UNIX
1. Create a Virtual Environment (`python3 -m venv <environment name>`)
2. Activate Virtual Environment (`source <environment name>/bin/activate`)
3. Install requirements.txt (`pip3 install -r requirements.txt`)



## Usage
1. Run `main.py` to start the chat application: `python main.py`.
2. Enter your queries in the application's chat window.
3. Responses from the GPT-RAG model will be displayed in the chat window.

## Configuration
- Environment variables should be set as per `env.template`.
- Logging levels and other configurations can be adjusted in `orchestrator_request.py`.

## Support
For any issues or queries, please open an issue in the repository or contact the development team.
