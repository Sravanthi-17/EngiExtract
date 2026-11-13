
from pypdf import PdfReader


def read_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    total_pages = len(reader.pages)

    print("PDF opened successfully!")
    print("Total pages:", total_pages)

    return reader
