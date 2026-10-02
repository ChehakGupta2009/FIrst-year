import fitz
from RAGPipeline import RAGPipeline 
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from urllib.parse import urlparse
import os


class Pdfparser:
    """Handles reading a PDF and building a simple RAG index for Q&A."""

    def readpdf(self, path):
        """Read a PDF from a local file path and return extracted page text."""
        try:
            pdf_obj = fitz.open(path)  # open PDF using PyMuPDF
            pages = []
            for i, page in enumerate(pdf_obj):
                pdf_text = page.get_text().strip()
                if pdf_text:
                    pages.append({"pageno.": i + 1, "text": pdf_text})
            return pages
        except Exception as e:
            raise ValueError(f"Failed to read PDF from path: {path}") from e

    def readPdfURL(self, url):
        """Download a PDF from a URL and return extracted page text."""
        try:
            resp = requests.get(url, timeout=30)  # download PDF content safely
            resp.raise_for_status()  # raise error if HTTP request fails
            pdf_file = BytesIO(resp.content)  # convert bytes into file-like object
            reader = PdfReader(pdf_file)
            pages = []
            for i, page in enumerate(reader):
                pdf_text = page.get_text().strip()
                if pdf_text:
                    pages.append({"pageno.": i + 1, "text": pdf_text})
            return pages
        except Exception as e:
            raise ValueError(f"Failed to read PDF from URL: {url}") from e
    def IsWebUrl(self,link: str) -> bool:
        link = link.strip()
        p = urlparse(link)
        check=False
        if p.scheme in ("http", "https", "ftp") and p.netloc:
            check=True
        if os.path.isabs(link) or os.path.exists(link):
            check=False
        return check
    def build_pdf_rag(self, path, groq_key):
        """Extract pages from a PDF and index them for RAG queries."""
        try:
            if self.IsWebUrl(path):
                pages = self.readPdfURL(path)
            else:
                pages = self.readpdf(path)
            documents = [page["text"] for page in pages]
            doc_name = [f"page_{page['pageno.']}" for page in pages]
            self.rag = RAGPipeline(groq_key)  # initialize the RAG pipeline
            self.rag.index(documents, doc_name)  # add PDF pages to the vector index
            print("PDF indexed successfully.")
        except Exception as e:
            print(f"Error building PDF RAG: {e}")
            self.rag = None

    def query(self):
        """Allow interactive question-and-answer queries against the indexed PDF."""
        if not hasattr(self, "rag") or self.rag is None:
            print("RAG is not initialized. Please build the PDF index first.")
            return

        print("Enter quit or exit to end the chat")
        while True:
            try:
                question = input("question:")
                if question.lower() in ["quit", "exit"]:
                    break
                answer = self.rag.query(question)
                print("answer:", answer)
            except KeyboardInterrupt:
                print("\nExiting chat.")
                break
            except Exception as e:
                print(f"Error while querying: {e}")


# Run only when this file is executed directly
if __name__ == "__main__":
    try:
        pdf=input("Enter the path or url of the file:")
        read_pdf = Pdfparser()
        read_pdf.build_pdf_rag(
            pdf,
            "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",
        )
        read_pdf.query()
    except Exception as e:
        print(f"Failed to initialize PDF parser: {e}")

