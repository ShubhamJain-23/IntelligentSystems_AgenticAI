# About PDF Search & RAG Tool

## Purpose
This tool was originally created for **Assignment 1** (PDF Semantic Similarity Search) and extended for **Assignment 3** to convert the CLI tool into a complete **Retrieval-Augmented Generation (RAG)** system.

Instead of merely printing the raw matching text chunk and similarity score, the system:
1. Retrieves the top-$k$ most semantically relevant text chunks from the document.
2. Pairs the user's query with the retrieved chunks: `(query, chunks)`.
3. Builds an **Augmented Prompt** containing the grounding context and strict instruction guardrails.
4. Submits the augmented prompt to a Large Language Model (LLM).
5. Displays both the **Augmented Prompt** sent to the LLM and the **Generated Response**.

---

## How the RAG Pipeline Works

The RAG architecture consists of four sequential stages:

### 1. Document Extraction & Contextual Chunking
- **Library:** `pypdf`
- **Process:** The tool extracts text page-by-page from the input PDF.
- **Unicode Sanitization:** Raw PDF streams often contain corrupted glyph encodings or unpaired UTF-16 surrogates (e.g. `\ud800`). The extractor sanitizes all strings to prevent tokenizer crashes.
- **Chunking Strategy:** Pages are split into bounded contextual chunks (up to 1,200 characters with 150-character sliding overlap for long pages) while preserving the exact page number of origin for citation.

### 2. Dense Semantic Retrieval
- **Library:** `sentence-transformers` & `torch`
- **Embedding Model:** `all-MiniLM-L6-v2` (384-dimensional dense vectors)
- **Process:**
  - Both the user's query and all document chunks are converted into dense vector embeddings.
  - Cosine similarity is computed between the query embedding and all chunk embeddings:
    $$\text{Similarity}(q, c_i) = \frac{\mathbf{e}_q \cdot \mathbf{e}_{c_i}}{\|\mathbf{e}_q\| \|\mathbf{e}_{c_i}\|}$$
  - The top-$k$ highest-scoring chunks are selected as the grounding context.

### 3. Prompt Augmentation `(query, chunks)`
- The system synthesizes the user question and the retrieved text chunks into a structured prompt:
  - **Context Block:** Clearly demarcated chunks labeled with their chunk ID and originating page numbers.
  - **Instructional Guardrails:** Directs the LLM to rely strictly on the provided context, avoid hallucinating external facts, cite page numbers, and explicitly state if the document lacks sufficient information.
  - **User Query:** Appends the user's specific question.

### 4. Generation & Display
- **SDK:** `openai`
- **Endpoints:** Compatible with local inference servers (LM Studio on `http://localhost:1234/v1`, Ollama on `http://localhost:11434/v1`) and OpenAI cloud endpoints.
- **Output:** The CLI renders:
  1. The complete **Augmented Prompt** sent over the wire to the model.
  2. The LLM's **Generated Response** answering the question based on the document.
