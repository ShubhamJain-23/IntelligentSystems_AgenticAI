# About PDF Search Tool

## Purpose
This tool was created for **Assignment-1**. 
It takes a large PDF document (e.g., ~100 pages) and a text query, then identifies and returns the page number and relevant text most similar to the query.

## How it Works
The application uses Natural Language Processing (NLP) techniques to measure text similarity:

1. **Text Extraction:** Uses the `pypdf` library to extract raw text from each page of the provided PDF.
2. **Vectorization:** Converts the text of each page and the search query into numerical vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)** via `scikit-learn`.
3. **Similarity Calculation:** Computes the **Cosine Similarity** between the query's vector and each page's vector to find the closest match. 
4. **Result:** The page with the highest similarity score is returned as the best match.
