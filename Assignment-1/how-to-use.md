# How to Use PDF Search Tool

This guide explains how to use the `pdf_search.py` command line tool to find the most relevant page in a PDF based on your query.

## Prerequisites
- Python 3.x installed
- Required packages installed (`pypdf`, `scikit-learn`, `numpy`)

If you haven't installed the dependencies, you can do so via:
```powershell
pip install pypdf scikit-learn numpy
```

## Running the Tool
Run the script from your command line:

```powershell
python pdf_search.py
```

The tool will then interactively prompt you to enter the path to the PDF and the search query:

```text
Welcome to the PDF Search Tool!

Please enter the path to your PDF file: C:\books\textbook.pdf
Please enter your search query: machine learning algorithms
```

## Output
The tool will output the page number that best matches your query along with an excerpt of the text from that page.
