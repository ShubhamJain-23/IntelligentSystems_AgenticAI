import sys
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)

    pages_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and isinstance(text, str) and text.strip():
            pages_text.append(text.strip())
        else:
            # Some tokenizers crash on completely empty strings.
            # We add a placeholder so the page index is maintained.
            pages_text.append("[NO EXTRACTABLE TEXT ON THIS PAGE]")
    return pages_text

def search_pdf(pdf_path, query):
    print(f"Reading PDF: {pdf_path}...")
    pages_text = extract_text_from_pdf(pdf_path)
    
    if not pages_text:
        print("No text found in the PDF.")
        return

    print("Loading AI model for semantic search (this may take a few seconds)...")
    # Import inside the function so the script starts up faster before prompting
    from sentence_transformers import SentenceTransformer, util
    import torch

    # Use a small, fast model excellent for semantic similarity
    # Note: On the very first run, this will download a ~80MB model to your cache
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Analyzing pages to understand the meaning of your query...")
    
    # Generate embeddings for the query and all pages
    page_emb_list = []
    fallback_emb = torch.zeros(384) # MiniLM embedding size
    
    for text in pages_text:
        # Truncate extremely long pages to prevent sequence length overflow
        safe_text = text[:8000]
        try:
            emb = model.encode(safe_text, convert_to_tensor=True)
            page_emb_list.append(emb)
        except Exception:
            # If a specific page has corrupted text/unicode that crashes the tokenizer, skip it
            page_emb_list.append(fallback_emb)
        
    page_embeddings = torch.stack(page_emb_list)
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # Compute Cosine Similarity based on meaning, not just exact keywords
    similarities = util.cos_sim(query_embedding, page_embeddings)[0]
    
    # Find the best page
    best_match_idx = torch.argmax(similarities).item()
    best_score = similarities[best_match_idx].item()

    if best_score < 0.15: # Arbitrary low threshold for confidence
         print(f"\nCould not find a highly relevant answer for your query. (Highest confidence score: {best_score:.4f})")
    else:
        page_num = best_match_idx + 1 # 1-based indexing for pages
        best_text = pages_text[best_match_idx]
        
        print("\n" + "="*70)
        print(f"✅ Best Match Found on Page: {page_num} (Semantic Relevance Score: {best_score:.4f})")
        print("="*70)
        print("\nExcerpt from the page:")
        
        display_text = best_text.strip()
        if len(display_text) > 1000:
            display_text = display_text[:1000] + "\n\n... [Text truncated]"
            
        print(display_text)
        print("\n" + "="*70)

if __name__ == "__main__":
    print("Welcome to the Semantic PDF Search Tool!\n")
    
    pdf_path = input("Please enter the path to your PDF file: ").strip()
    if pdf_path.startswith('"') and pdf_path.endswith('"'):
        pdf_path = pdf_path[1:-1]
    if pdf_path.startswith("'") and pdf_path.endswith("'"):
        pdf_path = pdf_path[1:-1]
        
    if not pdf_path:
        print("No PDF path provided. Exiting.")
        sys.exit(1)
        
    query = input("Please enter your search question: ").strip()
    
    if not query:
        print("No search question provided. Exiting.")
        sys.exit(1)
        
    print("\nStarting search...\n")
    search_pdf(pdf_path, query)
