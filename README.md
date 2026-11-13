# EngiExtract – Engineering Drawing PDF Extractor

## Project Overview
EngiExtract is a Python-based application designed to extract text and drawing regions from engineering drawing PDF files.

## Features
- Upload engineering drawing PDFs.
- Extract text from PDF pages.
- Extract embedded images.
- Detect drawing regions using OpenCV.
- Crop drawing regions separately.
- Process PDFs containing multiple pages.
- Display extracted text and drawing images using Streamlit.

## Technologies Used
- Python
- PyPDF
- PyMuPDF
- OpenCV
- NumPy
- Streamlit

## Project Structure
```text
EngiExtract/
├── app/
│   ├── app.py
│   ├── main.py
│   ├── pdf_reader.py
│   ├── text_extractor.py
│   ├── image_extractor.py
│   └── drawing_detector.py
├── output/
├── uploads/
├── requirements.txt
└── README.md
```

## How to Run

1. Clone the repository.
2. Open the project folder.
3. Create and activate a virtual environment.
4. Install the required packages:
   `pip install -r requirements.txt`
5. Run the application:
   `streamlit run app/app.py`

## Project Goal
To simplify the extraction of text and drawing regions from engineering drawing PDFs using Python-based image processing techniques.
