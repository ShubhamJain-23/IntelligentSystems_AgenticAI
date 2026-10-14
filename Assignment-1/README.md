# Assignment 1 & 3: PDF Similarity Search & RAG System

A command-line Retrieval-Augmented Generation (RAG) tool that extracts contextual chunks from a large PDF document, retrieves the most semantically relevant chunks for a user query using dense vector embeddings, constructs an augmented prompt containing `(query, chunks)`, and submits it to a Large Language Model (LLM) to output both the augmented prompt and the generated response.

> **Assignment 3 Update**: Upgraded the CLI tool from returning raw page chunks and similarity scores to a full **RAG system** that feeds retrieved chunks and query into an LLM, printing the complete augmented prompt and the generated answer.

## Key Features

- **Document Chunking & Sanitization:** Automatically parses PDF pages into contextual chunks while maintaining page number citations and cleaning Unicode encodings.
- **Dense Semantic Retrieval:** Uses `sentence-transformers/all-MiniLM-L6-v2` with PyTorch to compute cosine similarity in high-dimensional semantic vector space.
- **Prompt Augmentation:** Structures retrieved chunks and the user's question into an explicit, grounded prompt template.
- **LLM Integration:** Connects seamlessly via the OpenAI SDK to local inference servers (LM Studio, Ollama) or remote OpenAI-compatible endpoints.
- **Dual Output:** Outputs both the **Augmented Prompt sent to the LLM** and the **Generated Response**.
- **Offline / Mock Mode:** Includes `--mock` flag for offline testing and development without a running LLM server.

## Documentation

- [About](about.md) - Details on the internal workings, RAG methodology, and prompt engineering.
- [How to Use](how-to-use.md) - Setup guide, CLI arguments, and example runs with output.
- [Architecture](architecture.md) - Software and technical architecture, detailing the evolution from TF-IDF to Semantic Search to RAG.

## Setup

To set up the environment, activate the virtual environment and install the required dependencies:

```powershell
.\.venv\Scripts\activate
pip install pypdf sentence-transformers torch openai
```

## Quick Start

### 1. Interactive Mode
```powershell
python pdf_search.py
```
The tool will prompt you for the PDF path and query.

### 2. Command Line Arguments
```powershell
python pdf_search.py --pdf TestPDF.pdf --query "What is a function in Python?" --top-k 2
```

### 3. Offline / Test Mode
```powershell
python pdf_search.py --pdf TestPDF.pdf --query "What is a function in Python?" --mock
```
