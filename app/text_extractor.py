
def extract_text_from_pdf(reader):

    extracted_pages = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        page_data = {
            "page_number": page_number + 1,
            "text": text if text else ""
        }

        extracted_pages.append(page_data)

    print("Text extraction completed!")
    print("Pages processed:", len(extracted_pages))

    return extracted_pages
