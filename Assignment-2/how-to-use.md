# How to Use Bot-to-Bot Chat Application

This guide explains how to configure and run the `chat_app.py` script.

## Prerequisites
- Python 3.x installed
- Virtual environment with the `openai` Python package installed
- A local AI inference server (e.g., LM Studio, Ollama, bionic endpoint) running and serving an OpenAI-compatible API on `http://localhost:1234/v1`

## Setup
If you haven't installed the dependencies yet, navigate to your project root and install the required package:
```powershell
.\.venv\Scripts\activate
pip install openai
```

## Running the Application
Ensure your local server is running and accessible, then execute the script from the command line:
```powershell
cd Assignment-2
python chat_app.py
```

When you run the script, you will be prompted to:
1. **Enter a seed message:** This is the starting topic or question that Agent 1 will ask Agent 2.
2. **Enter the number of rounds:** Provide an integer to dictate how many back-and-forth exchanges the bots should have. (Leave it blank and press Enter to default to 5).

## Viewing Chat History
After the application finishes running, your entire conversation will be formatted as a JSON file and saved inside the `chat_history/` directory. The files are uniquely named using the current timestamp (e.g., `chat_log_20261009_124045.json`), so previous conversations are never overwritten.

## Customization Options
You can directly tweak the following configurations inside `chat_app.py`:
- `MODEL_NAME`: Set this to your specific local model string (defaults to `"qwen/qwen3-4b"`).
- **System Prompts**: Edit the `bot1_system_prompt` and `bot2_system_prompt` strings to fundamentally change the agent personalities or generation constraints.
