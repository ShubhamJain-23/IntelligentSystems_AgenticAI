# Assignment 2 - Bot to Bot Chat

This assignment demonstrates a chat application where two bots talk to each other. 
The bots are powered by the OpenAI SDK and communicate with a language model via a local server (like LM Studio or a similar "bionic" local inference setup).

## Documentation
- [Architecture](architecture.md) - Overview of the software and technical architecture.
- [About](about.md) - Details on the internal workings and methodology of the chat application.
- [How to Use](how-to-use.md) - Instructions on setting up, customizing, and running the application.

## Setup
To set up the environment, you can use the same virtual environment created in Assignment-1:
```powershell
..\venv\Scripts\activate
pip install openai
```

## Running the Application
Ensure that your local inference server (e.g. your bionic model endpoint) is running and accessible. By default, the script connects to `http://localhost:1234/v1` (the default LM Studio port).

To run the chat application:
```powershell
python chat_app.py
```

## How it works
1. **Dynamic Inputs:** When run, the script prompts the user to enter a seed message to start the conversation, as well as the desired number of conversational rounds.
2. **Bot Personalities:** Two distinct personalities are provided to the bots via System Prompts (e.g., a Philosopher vs. a Scientist). The bots are explicitly instructed to keep their responses extremely concise.
3. **Iteration:** The script runs a back-and-forth loop for the requested number of iterations. Each bot receives the other's message, updates its internal context window (chat history), and generates a new reply using the `client.chat.completions.create` API.
4. **Chat History Export:** After the conversation completes, the entire transcript is automatically saved as a uniquely timestamped JSON file in the `chat_history/` directory.
