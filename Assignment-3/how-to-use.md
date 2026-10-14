# How to Use Assignment 3: RAG System

This guide covers running the Assignment 3 RAG CLI tool, configuring the LLM connection, and inspecting results.

---

## Prerequisites

1. Activate your virtual environment:
   ```powershell
   ..\.venv\Scripts\activate
   ```
2. Verify required packages:
   ```powershell
   pip install pypdf sentence-transformers torch openai
   ```

---

## LLM Server Configuration

By default, the script connects to `http://localhost:1234/v1` with model `qwen/qwen3-4b` (standard LM Studio configuration used in Assignment 2).

### Option 1: LM Studio (Local Inference)
- Launch **LM Studio**.
- Load a local model (e.g. `qwen/qwen3-4b` or `google/gemma-4-e4b`).
- Start the local server on port `1234`.

### Option 2: Ollama (Local Inference)
- Run `ollama run qwen2.5:3b`.
- Run the tool specifying `--base-url http://localhost:11434/v1 --model qwen2.5:3b`.

### Option 3: Remote OpenAI API
- Set environment variables:
  ```powershell
  $env:OPENAI_API_KEY = "your-api-key"
  $env:OPENAI_BASE_URL = "https://api.openai.com/v1"
  $env:OPENAI_MODEL_NAME = "gpt-4o-mini"
  ```

### Option 4: Mock Mode (Offline Testing)
- Run with `--mock` to verify the pipeline without a running inference server.

---

## Running the Application

### Method 1: Interactive Prompts
Run without arguments:
```powershell
python rag_search.py
```
Input the PDF path (e.g., `TestPDF.pdf`) and search question when prompted.

### Method 2: Command-Line Arguments
```powershell
python rag_search.py --pdf TestPDF.pdf --query "What is a function in Python?" --top-k 2
```

### CLI Flag Reference
- `--pdf`: Path to the PDF file.
- `--query`: User question.
- `--top-k`: Number of chunks to retrieve (default: `3`).
- `--base-url`: LLM API endpoint (default: `http://localhost:1234/v1`).
- `--api-key`: API key (default: `dummy_api_key`).
- `--model`: Model identifier (default: `qwen/qwen3-4b`).
- `--mock`: Flag to simulate LLM responses for offline execution.

---

## Output Format

The tool prints:
1. **Extraction and Retrieval Summary** (chunk counts and cited pages).
2. **AUGMENTED PROMPT SENT TO LLM** (the complete formatted prompt provided to the model).
3. **GENERATED RESPONSE** (the model's generated answer).
