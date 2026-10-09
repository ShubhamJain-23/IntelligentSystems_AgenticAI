# Assignment 1: PDF Similarity Search

A command-line tool that outputs the page number and relevant text from a large PDF that is most similar to a given query.

## Documentation

- [About](about.md) - Details on the internal workings and methodology of the tool.
- [How to Use](how-to-use.md) - Instructions on setting up and running the tool.
- [Architecture](architecture.md) - Detailed software and technical architecture, including our design evolution.

## Setup
To set up the environment, run these commands in the root directory:
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install pypdf scikit-learn numpy
```
