# Project Architecture: PDF Search Tool

## Overview
The PDF Search Tool is a lightweight, command-line application designed to find the most relevant page in a large PDF document (e.g., 100+ pages) given a user's text query.

## Software Architecture
The application is structured as a single-script Python program (`pdf_search.py`). The logic is divided into modular functions to separate concerns:

1. **User Interface / I/O Handling:** Handles interactive command-line prompts and input validation (e.g., gracefully handling drag-and-dropped file paths with quotes).
2. **Document Parsing (`extract_text_from_pdf`):** Interfaces with the file system and uses the `pypdf` library to parse and extract text from the PDF. It returns a structured list of strings where each index corresponds to a page.
3. **Core Search Engine (`search_pdf`):** Takes the extracted text and the user's query, transforms both into a shared vector space, computes mathematical similarities, and returns the highest-scoring page with a contextual snippet.

---

## Technical Architecture (The Search Engine)

The core technical architecture has evolved during the development of this assignment to better handle natural language questions. 

### Initial Approach: TF-IDF (Lexical Search)
Initially, the tool was built using **Term Frequency-Inverse Document Frequency (TF-IDF)** and Cosine Similarity via `scikit-learn`.
* **How it worked:** It vectorized the text based on the statistical frequency of words. It counted the occurrences of words in the query and compared them to the occurrences of those same words on each page.
* **Why we changed it:** TF-IDF relies entirely on *exact keyword matching*. If a user asked a conceptual question like "What are the risks of database exploits?", TF-IDF would strictly look for the exact words "risks", "database", and "exploits". It would completely fail to find a page discussing "SQL injection vulnerabilities" because it lacks the ability to understand that the concepts are semantically related. This resulted in poor performance for conversational questions.

### Current Approach: Semantic Search (Dense Embeddings)
To solve the limitations of lexical search, we upgraded the engine to use **Semantic Search** via `sentence-transformers` and PyTorch (`torch`).
* **How it works:** 
  1. **Vector Embeddings:** We use a pre-trained Large Language Model (LLM) tailored for embeddings to encode both the user's query and the text of each PDF page into high-dimensional dense vectors.
  2. **Cosine Similarity:** We calculate the cosine similarity between the query vector and all page vectors to find the closest point in the semantic space.
* **Why we did this:** Transformer models understand the *meaning* and *context* of language. By converting text into semantic vectors, the system can map a question to an answer even if they share zero exact keywords. 
* **Model Selection:** The `all-MiniLM-L6-v2` model was chosen specifically because it offers a perfect balance for this use case: it provides excellent semantic similarity mapping while being highly optimized, fast, and having a very small memory footprint (~80MB), making it ideal for a local command-line tool.
