
import pymupdf
import os


def render_pdf_pages(pdf_path):

    doc = pymupdf.open(pdf_path)

    output_folder = "../output/rendered_pages"
    os.makedirs(output_folder, exist_ok=True)

    for page_number, page in enumerate(doc):

        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2)
        )

        image_path = os.path.join(
            output_folder,
            f"page_{page_number + 1}.png"
        )

        pix.save(image_path)

        print(f"Page {page_number + 1} rendered successfully!")

    doc.close()


def extract_embedded_images(pdf_path):

    doc = pymupdf.open(pdf_path)

    output_folder = "../output/embedded_images"
    os.makedirs(output_folder, exist_ok=True)

    for page_number, page in enumerate(doc):

        images = page.get_images(full=True)

        for image_number, image in enumerate(images):

            xref = image[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            image_extension = base_image["ext"]

            image_path = os.path.join(
                output_folder,
                f"page_{page_number + 1}_image_{image_number + 1}.{image_extension}"
            )

            with open(image_path, "wb") as file:
                file.write(image_bytes)

            print(f"Image extracted: {image_path}")

    doc.close()

    print("Embedded image extraction completed!")
