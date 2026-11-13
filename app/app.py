import stat
import streamlit as st
import os
import requests
import shutil
from pdf_reader import read_pdf
from text_extractor import extract_text_from_pdf
from drawing_detector import process_all_pages


def handle_remove_readonly(func, path, exc_info):

    os.chmod(path, stat.S_IWRITE)
    func(path)


def clear_previous_outputs():

    output_folders = [
        "../output/grayscale",
        "../output/threshold",
        "../output/contours",
        "../output/bounding_boxes",
        "../output/cropped_drawings",
        "../output/embedded_images",
        "../output/rendered_pages"
    ]

    for folder in output_folders:

        if os.path.exists(folder):

            shutil.rmtree(
                folder,
                onerror=handle_remove_readonly
            )

        os.makedirs(folder, exist_ok=True)

    print("Previous PDF outputs cleared!")



# PAGE CONFIGURATION
st.set_page_config(
    page_title="EngiExtract",
    page_icon="📐",
    layout="wide"
)


# APPLICATION TITLE
st.title("📐 EngiExtract")
st.subheader("Engineering PDF Text & Drawing Extraction System")

st.write(
    "Upload an engineering PDF or provide a PDF URL "
    "to extract text and drawing regions separately."
)


# INPUT OPTIONS
st.header("Upload Engineering PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

pdf_url = st.text_input(
    "Or enter a PDF URL"
)


# PROCESS BUTTON
if st.button("Extract PDF Content"):

    pdf_path = "../uploads/input.pdf"
    os.makedirs("../uploads", exist_ok=True)

    # OPTION 1: UPLOAD PDF
    if uploaded_file is not None:

        with open(pdf_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

    # OPTION 2: DOWNLOAD PDF FROM URL
    elif pdf_url.strip():

        try:
            response = requests.get(
                pdf_url,
                timeout=30
            )

            response.raise_for_status()

            if not response.content.startswith(b"%PDF-"):
                st.error("The provided URL does not return a valid PDF.")
                st.stop()

            with open(pdf_path, "wb") as file:
                file.write(response.content)

        except requests.RequestException as error:
            st.error(f"PDF download failed: {error}")
            st.stop()

    else:
        st.warning("Please upload a PDF or enter a PDF URL.")
        st.stop()

    # PROCESS PDF
    try:
        clear_previous_outputs()
        with st.spinner("Processing your PDF..."):

            reader = read_pdf(pdf_path)

            extracted_pages = extract_text_from_pdf(reader)

            process_all_pages(pdf_path)

        st.success("PDF processing completed successfully!")

        # DISPLAY RESULTS PAGE BY PAGE
        st.header("Extraction Results")

        for page_data in extracted_pages:

            page_number = page_data["page_number"]

            st.divider()

            st.subheader(f"Page {page_number}")

            col1, col2 = st.columns(2)

            # DISPLAY TEXT
            with col1:

                st.markdown("### Extracted Text")

                page_text = page_data["text"]

                if page_text.strip():
                    st.text_area(
                        "PDF Text",
                        page_text,
                        height=350,
                        key=f"text_{page_number}"
                    )
                else:
                    st.info("No selectable text found on this page.")

            # DISPLAY DRAWING
            with col2:

                st.markdown("### Extracted Drawing")

                image_path = (
                    f"../output/cropped_drawings/"
                    f"page_{page_number}_drawing_1.png"
                )

                if os.path.exists(image_path):

                    st.image(
                        image_path,
                        caption=f"Page {page_number} drawing",
                        use_container_width=True
                    )

                else:
                    st.info("No drawing region was detected.")

        st.success("EngiExtract finished!")

    except Exception as error:
        st.error(f"Processing failed: {error}")
