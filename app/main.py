
import os

from pdf_reader import read_pdf
from text_extractor import extract_text_from_pdf
from drawing_detector import process_all_pages


# PDF input
pdf_path = "../uploads/sample.pdf"


# STEP 1: Read PDF
reader = read_pdf(pdf_path)


# STEP 2: Extract text from all pages
extracted_pages = extract_text_from_pdf(reader)


# STEP 3: Process drawings from all pages
process_all_pages(pdf_path)


# STEP 4: Display extracted text page by page
for page_data in extracted_pages:

    print("\n================================")
    print("PAGE:", page_data["page_number"])
    print("================================")

    print(page_data["text"])


print("\nEngiExtract processing completed!")
