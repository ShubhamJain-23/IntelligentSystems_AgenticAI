# How to Use the PDF RAG Tool

This guide explains how to run and configure the `pdf_search.py` Retrieval-Augmented Generation (RAG) command-line tool.

---

## 1. Prerequisites & Installation

Activate your virtual environment and ensure all dependencies are installed:

```powershell
.\.venv\Scripts\activate
pip install pypdf sentence-transformers torch openai
```

---

## 2. LLM Server Setup (Optional for Live Generation)

By default, the tool communicates with an OpenAI-compatible endpoint at `http://localhost:1234/v1` (the default LM Studio port, matching Assignment 2).

### Option A: LM Studio (Local Inference)
1. Open **LM Studio**.
2. Download or select a model (e.g. `qwen/qwen3-4b` or `google/gemma-4-e4b`).
3. Start the local server on port `1234`.

### Option B: Ollama (Local Inference)
Run Ollama with your chosen model:
```powershell
ollama run qwen2.5:3b
```
And pass `--base-url http://localhost:11434/v1 --model qwen2.5:3b` when running `pdf_search.py`.

### Option C: OpenAI Cloud API
Set your API key in PowerShell:
```powershell
$env:OPENAI_API_KEY="sk-..."
$env:OPENAI_BASE_URL="https://api.openai.com/v1"
$env:OPENAI_MODEL_NAME="gpt-4o-mini"
```

### Option D: Offline / Mock Mode (No server needed)
Pass the `--mock` flag to run the entire pipeline offline without requiring any LLM server.

---

## 3. Running the Tool

### Method 1: Interactive Mode
Simply run the script with no arguments:
```powershell
python pdf_search.py
```
You will be prompted to enter the path to the PDF and your question:
```text
Welcome to the PDF RAG System!

Please enter the path to your PDF file: TestPDF.pdf
Please enter your search question: What is a function in Python and how do you define one?
```

### Method 2: Command-Line Arguments
You can supply all arguments directly via the terminal:

```powershell
python pdf_search.py --pdf TestPDF.pdf --query "What is a function in Python?" --top-k 2
```

### Available CLI Flags

| Flag | Default | Description |
|---|---|---|
| `--pdf` | *(interactive prompt)* | File path to the target PDF document. |
| `--query` | *(interactive prompt)* | Natural language question to ask. |
| `--top-k` | `3` | Number of most relevant context chunks to retrieve. |
| `--base-url` | `http://localhost:1234/v1` | Base URL of the OpenAI-compatible server. |
| `--api-key` | `dummy_api_key` | API key for authentication. |
| `--model` | `qwen/qwen3-4b` | Model name to query on the server. |
| `--mock` | `False` | Run in offline demonstration mode. |

---

## 4. Example Output

When executed, the tool outputs both the **Augmented Prompt** sent to the LLM and the **Generated Response**:

```text
1. Reading & chunking PDF: 'TestPDF.pdf'...
   -> Extracted 267 contextual text chunk(s).

2. Retrieving top 2 most relevant chunk(s) for query: 'What is a function in Python?'...
Loading embedding model for retrieval (all-MiniLM-L6-v2)...
Analyzing 267 contextual chunks against query...
   -> Retrieved 2 chunk(s) from Page(s): [45]

3. Building Augmented Prompt combining (query, chunks)...

4. Querying LLM with Augmented Prompt...

================================================================================
                      AUGMENTED PROMPT SENT TO LLM                      
================================================================================
You are an expert AI assistant that answers questions accurately based on the provided document context.

Instructions:
1. Answer the question relying ONLY on the provided context chunks below.
2. Keep your answer factual, concise, and clear.
3. Explicitly cite the page number(s) where the supporting information was found.
4. If the provided context does not contain sufficient information to answer the question, state clearly: 'The provided document does not contain sufficient information to answer this question.'

==================== RETRIEVED CONTEXT ====================
[Context Chunk 1 | Page 45]
Functions Functions are reusable pieces of programs. They allow you to give a name to a block of statements, allowing you to run that block using the specified name anywhere in your program and any number of times. This is known as calling the function... Functions are defined using the def keyword. After this keyword comes an identifier name for the function, followed by a pair of parentheses which may enclose some names of variables, and by the final colon that ends the line...

[Context Chunk 2 | Page 45]
ames given in the function definition are called parameters whereas the values you supply in the function call are called arguments...
===========================================================

User Query: What is a function in Python?

Answer:
================================================================================

================================================================================
                           GENERATED RESPONSE                           
================================================================================
A function in Python is a reusable block of code that can be executed anywhere in a program using its specified name. Functions are defined using the 'def' keyword, followed by an identifier name, a pair of parentheses (which may enclose parameter names), and a colon. (Source: Page 45)
================================================================================
```
