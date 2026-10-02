# PDFQnA

This folder contains a simple PDF-based question answering project using a Retrieval-Augmented Generation (RAG) pipeline.

## What this project does

The project loads text from a PDF, splits it into chunks, stores those chunks in a vector database, and then answers user questions based on the most relevant parts of the PDF.

It combines:
- PDF extraction
- text chunking
- vector search
- Groq-based LLM responses

---

## Files in this folder

### `PDFParser.py`
This file is responsible for reading PDF content and preparing it for indexing.

It includes:
- local PDF reading with `fitz`
- URL-based PDF download with `requests`
- detection of web URLs vs local file paths
- building the RAG index
- interactive Q&A through the console

### `RAGPipeline.py`
This file contains the retrieval and generation logic.

It includes:
- creating a ChromaDB collection
- splitting documents into chunks
- indexing documents and metadata
- retrieving the most relevant chunks for a question
- sending the context to the Groq model for answer generation

---

## How it works

1. A PDF file or URL is passed to `Pdfparser`.
2. The PDF text is extracted page by page.
3. The content is split into smaller chunks.
4. Each chunk is added to a ChromaDB collection.
5. When a question is asked, the system finds the most relevant chunks.
6. Those chunks are sent to the Groq language model as context.
7. The model answers using only the available context.

---

## Main usage

Run the script in `PDFParser.py`:

```python
if __name__ == "__main__":
    pdf = input("Enter the path or url of the file:")
    read_pdf = Pdfparser()
    read_pdf.build_pdf_rag(pdf, "YOUR_GROQ_API_KEY")
    read_pdf.query()
```

This will:
- ask for a PDF path or URL
- build the RAG index
- start a chat loop for asking questions

---

## Requirements

This project depends on:
- `fitz`
- `PyPDF2`
- `requests`
- `chromadb`
- `groq`
- `sentence-transformers` / embedding support

Make sure these packages are installed before running the project.

---

## Notes

- The project is meant for learning and experimentation.
- The RAG logic is simple and can be improved with better chunking, metadata handling, and model tuning.
- The query method uses a console-based interface.

---

## Example flow

```python
from PDFParser import Pdfparser

pdf_reader = Pdfparser()
pdf_reader.build_pdf_rag("your_file.pdf", "your_api_key")
pdf_reader.query()
```

This is useful for asking questions like:
- "What is this PDF about?"
- "Summarize the key points from page 2."
- "What are the instructions mentioned in the document?"

---

## Summary

This folder is a small PDF Q&A application built around a RAG pattern. It demonstrates how to turn a PDF into searchable knowledge and answer questions from it using an LLM.
