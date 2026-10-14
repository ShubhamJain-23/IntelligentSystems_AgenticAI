# Assignment 3: Retrieval-Augmented Generation (RAG) System

This assignment continues building upon the command-line search tool from Assignment 1, converting it into a full **Retrieval-Augmented Generation (RAG)** system.

Instead of merely printing the most relevant raw chunk and its similarity score, the system takes `(query, chunks)`, constructs an **Augmented Prompt** containing the grounding context and instructions, feeds it to a Large Language Model (LLM), and outputs the complete augmented prompt along with the model's generated response.

---

## Documentation

- [About](about.md) - Internal workings, RAG methodology, chunking, and prompt engineering.
- [How to Use](how-to-use.md) - Instructions on setting up, configuring LLM endpoints, and executing the tool.
- [Architecture](architecture.md) - System architecture, component breakdowns, and data flow diagrams.

---

## Setup

Activate the virtual environment and ensure dependencies are installed:

```powershell
..\.venv\Scripts\activate
pip install pypdf sentence-transformers torch openai
```

---

## How It Works

1. **Document Ingestion & Chunking:** Reads a large PDF document (e.g. `TestPDF.pdf`), cleans corrupted encodings/surrogates, and slices pages into contextual chunks while tracking page numbers.
2. **Dense Vector Retrieval:** Uses `all-MiniLM-L6-v2` dense embeddings to perform semantic search, retrieving top-$k$ relevant chunks for the user's query.
3. **Prompt Augmentation:** Structures `(query, chunks)` into an explicit prompt containing the retrieved context, instructions to prevent hallucination, and the user's query.
4. **LLM Generation:** Sends the prompt to an LLM via the OpenAI SDK (compatible with LM Studio, Ollama, or OpenAI API).
5. **Dual Output:** Prints both the **Augmented Prompt sent to the LLM** and the **Generated Response**.

---

## Running the Application

### Interactive Execution
```powershell
python rag_search.py
```
Prompts for the PDF path and the search question.

### Command-Line Arguments
```powershell
python rag_search.py --pdf TestPDF.pdf --query "What is a function in Python?" --top-k 2
```

### Offline / Mock Mode (Testing without active server)
```powershell
python rag_search.py --pdf TestPDF.pdf --query "What is a function in Python?" --mock
```
