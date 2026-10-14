import os
import sys
import argparse
from pypdf import PdfReader
from openai import OpenAI

def extract_chunks_from_pdf(pdf_path, max_chunk_chars=1200, overlap=150):
    """
    Extracts text from each page of a PDF document, sanitizes Unicode (stripping
    unpaired surrogates), and splits it into manageable contextual chunks while
    preserving page number attribution.
    
    Returns:
        list of dict: Each item contains {'chunk_id': int, 'page': int, 'text': str}
    """
    try:
        reader = PdfReader(pdf_path)
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)

    chunks = []
    chunk_counter = 1

    for page_idx, page in enumerate(reader.pages):
        page_num = page_idx + 1
        raw_text = page.extract_text()
        if not raw_text or not isinstance(raw_text, str) or not raw_text.strip():
            continue

        # Sanitize UTF-8 to remove any unpaired surrogates or unencodable characters
        clean_text = raw_text.encode("utf-8", "ignore").decode("utf-8")
        clean_text = " ".join(clean_text.split())
        if not clean_text:
            continue

        # If the page text is reasonably sized, keep it as a single chunk
        if len(clean_text) <= max_chunk_chars:
            chunks.append({
                "chunk_id": chunk_counter,
                "page": page_num,
                "text": clean_text
            })
            chunk_counter += 1
        else:
            # For longer pages, create overlapping text chunks to maintain context
            start = 0
            while start < len(clean_text):
                end = min(start + max_chunk_chars, len(clean_text))
                # Adjust end to boundary of word if possible
                if end < len(clean_text):
                    last_space = clean_text.rfind(" ", start, end)
                    if last_space > start:
                        end = last_space
                
                chunk_slice = clean_text[start:end].strip()
                if chunk_slice:
                    chunks.append({
                        "chunk_id": chunk_counter,
                        "page": page_num,
                        "text": chunk_slice
                    })
                    chunk_counter += 1
                
                if end >= len(clean_text):
                    break
                start = end - overlap if (end - overlap) > start else end

    return chunks

def retrieve_relevant_chunks(chunks, query, top_k=3, model_name="all-MiniLM-L6-v2"):
    """
    Computes semantic similarity between the query and document chunks
    using dense embeddings from sentence-transformers.
    
    Returns:
        list of tuple: (chunk_dict, similarity_score) for top_k chunks.
    """
    if not chunks:
        return []

    print("Loading embedding model for retrieval (all-MiniLM-L6-v2)...")
    from sentence_transformers import SentenceTransformer, util
    import torch

    model = SentenceTransformer(model_name)
    
    clean_query = query.encode("utf-8", "ignore").decode("utf-8")
    query_embedding = model.encode(clean_query, convert_to_tensor=True, show_progress_bar=False)

    print(f"Analyzing {len(chunks)} contextual chunks against query...")
    
    # Encode chunks with individual fallback in case of tokenization anomalies
    embeddings_list = []
    fallback_emb = torch.zeros(384)
    for c in chunks:
        safe_text = c["text"][:4000]
        try:
            emb = model.encode(safe_text, convert_to_tensor=True, show_progress_bar=False)
            embeddings_list.append(emb)
        except Exception:
            embeddings_list.append(fallback_emb)

    chunk_embeddings = torch.stack(embeddings_list)

    # Compute cosine similarities
    similarities = util.cos_sim(query_embedding, chunk_embeddings)[0]

    # Select top-k highest scoring indices
    k = min(top_k, len(chunks))
    top_results = torch.topk(similarities, k=k)
    
    retrieved = []
    for score, idx in zip(top_results.values, top_results.indices):
        chunk_obj = chunks[idx.item()]
        retrieved.append((chunk_obj, score.item()))

    return retrieved

def build_augmented_prompt(query, chunks):
    """
    Constructs the augmented prompt combining the retrieved context chunks
    and the user query to supply to the LLM.
    
    Parameters:
        query (str): The user query/question.
        chunks (list of dict): Retrieved chunks containing 'page' and 'text'.
        
    Returns:
        str: The full augmented prompt.
    """
    context_sections = []
    for i, chunk in enumerate(chunks, 1):
        context_sections.append(
            f"[Context Chunk {i} | Page {chunk.get('page', 'Unknown')}]\n"
            f"{chunk['text']}"
        )
    
    joined_context = "\n\n".join(context_sections)

    augmented_prompt = (
        "You are an expert AI assistant that answers questions accurately based on the provided document context.\n\n"
        "Instructions:\n"
        "1. Answer the question relying ONLY on the provided context chunks below.\n"
        "2. Keep your answer factual, concise, and clear.\n"
        "3. Explicitly cite the page number(s) where the supporting information was found.\n"
        "4. If the provided context does not contain sufficient information to answer the question, state clearly: "
        "'The provided document does not contain sufficient information to answer this question.'\n\n"
        f"==================== RETRIEVED CONTEXT ====================\n"
        f"{joined_context}\n"
        f"===========================================================\n\n"
        f"User Query: {query}\n\n"
        f"Answer:"
    )
    return augmented_prompt

def generate_llm_response(augmented_prompt, base_url=None, api_key=None, model_name=None, mock=False, chunks=None):
    """
    Submits the augmented prompt to an LLM via the OpenAI-compatible API
    (e.g., LM Studio local server, Ollama, or OpenAI) and retrieves the generated completion.
    
    Returns:
        str: The generated response.
    """
    if mock:
        sample_page = chunks[0]['page'] if chunks else 1
        sample_text = chunks[0]['text'][:300] if chunks else ""
        return (
            f"[Offline / Mock LLM Response]\n"
            f"Based on the provided context from Page {sample_page}:\n\n"
            f"{sample_text}...\n\n"
            f"(Source: Page {sample_page})"
        )

    base_url = base_url or os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1")
    api_key = api_key or os.getenv("OPENAI_API_KEY", "dummy_api_key")
    model_name = model_name or os.getenv("OPENAI_MODEL_NAME", "qwen/qwen3-4b")

    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers queries strictly using the provided context."
                },
                {
                    "role": "user",
                    "content": augmented_prompt
                }
            ],
            temperature=0.3,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = (
            f"[Unable to connect to LLM server at '{base_url}']\n"
            f"Details: {e}\n\n"
            f"To generate live LLM responses:\n"
            f"1. Start your local inference server (e.g. LM Studio on port 1234 or Ollama).\n"
            f"2. Ensure model '{model_name}' is loaded.\n"
            f"3. Alternatively, specify --base-url, --api-key, and --model, or set them via environment variables.\n"
            f"4. You can also run with --mock for offline testing of the RAG pipeline."
        )
        return error_msg

def rag_search(pdf_path, query, top_k=3, base_url=None, api_key=None, model_name=None, mock=False):
    """
    Executes the complete Retrieval-Augmented Generation (RAG) pipeline:
    1. Extract and chunk text from the PDF.
    2. Retrieve top-k relevant chunks using dense semantic embeddings.
    3. Build an augmented prompt containing (query, chunks).
    4. Query the LLM with the augmented prompt.
    5. Output the augmented prompt and generated response.
    """
    print(f"\n1. Reading & chunking PDF: '{pdf_path}'...")
    chunks = extract_chunks_from_pdf(pdf_path)
    
    if not chunks:
        print("Error: No extractable text found in the PDF.")
        return

    print(f"   -> Extracted {len(chunks)} contextual text chunk(s).")

    print(f"\n2. Retrieving top {top_k} most relevant chunk(s) for query: '{query}'...")
    retrieved_results = retrieve_relevant_chunks(chunks, query, top_k=top_k)
    
    if not retrieved_results:
        print("Could not retrieve relevant chunks.")
        return

    selected_chunks = [item[0] for item in retrieved_results]
    pages_cited = sorted(list(set(c['page'] for c in selected_chunks)))
    print(f"   -> Retrieved {len(selected_chunks)} chunk(s) from Page(s): {pages_cited}")

    print("\n3. Building Augmented Prompt combining (query, chunks)...")
    augmented_prompt = build_augmented_prompt(query, selected_chunks)

    print("\n4. Querying LLM with Augmented Prompt...")
    generated_response = generate_llm_response(
        augmented_prompt,
        base_url=base_url,
        api_key=api_key,
        model_name=model_name,
        mock=mock,
        chunks=selected_chunks
    )

    # Output the Augmented Prompt along with the Generated Response
    print("\n" + "=" * 80)
    print("                      AUGMENTED PROMPT SENT TO LLM                      ")
    print("=" * 80)
    print(augmented_prompt)
    print("=" * 80)

    print("\n" + "=" * 80)
    print("                           GENERATED RESPONSE                           ")
    print("=" * 80)
    print(generated_response)
    print("=" * 80 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="RAG PDF Search Tool: Retrieves relevant chunks from a PDF, augments a prompt with (query, chunks), and queries an LLM."
    )
    parser.add_argument("--pdf", type=str, help="Path to the PDF file")
    parser.add_argument("--query", type=str, help="Question/query to ask about the PDF")
    parser.add_argument("--top-k", type=int, default=3, help="Number of relevant chunks to retrieve (default: 3)")
    parser.add_argument("--base-url", type=str, default=None, help="LLM API base URL (default: http://localhost:1234/v1)")
    parser.add_argument("--api-key", type=str, default=None, help="API key for LLM server (default: dummy_api_key)")
    parser.add_argument("--model", type=str, default=None, help="Model name (default: qwen/qwen3-4b)")
    parser.add_argument("--mock", action="store_true", help="Run with simulated LLM response for offline testing")

    args = parser.parse_args()

    pdf_path = args.pdf
    query = args.query

    # Interactive prompts if arguments are not provided via CLI
    if not pdf_path:
        print("Welcome to the PDF RAG System!\n")
        pdf_path = input("Please enter the path to your PDF file: ").strip()
        if pdf_path.startswith('"') and pdf_path.endswith('"'):
            pdf_path = pdf_path[1:-1]
        if pdf_path.startswith("'") and pdf_path.endswith("'"):
            pdf_path = pdf_path[1:-1]

    if not pdf_path:
        print("No PDF path provided. Exiting.")
        sys.exit(1)

    if not query:
        query = input("Please enter your search question: ").strip()

    if not query:
        print("No search question provided. Exiting.")
        sys.exit(1)

    rag_search(
        pdf_path=pdf_path,
        query=query,
        top_k=args.top_k,
        base_url=args.base_url,
        api_key=args.api_key,
        model_name=args.model,
        mock=args.mock
    )

if __name__ == "__main__":
    main()
