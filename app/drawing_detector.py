
import cv2
import os
import pymupdf


# Project output folders
OUTPUT_FOLDER = "../output"


# STEP 1: Process every PDF page
def process_all_pages(pdf_path):

    doc = pymupdf.open(pdf_path)

    print("PDF opened successfully!")
    print("Total pages:", len(doc))

    for page_index, page in enumerate(doc):

        page_number = page_index + 1

        print(f"\nProcessing page {page_number}...")

        # Render PDF page as image
        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2)
        )

        image = pix.tobytes("png")

        import numpy as np
        image_array = np.frombuffer(image, dtype=np.uint8)
        original_image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        # STEP 2: Save grayscale image
        gray_image = cv2.cvtColor(
            original_image,
            cv2.COLOR_BGR2GRAY
        )

        grayscale_folder = os.path.join(
            OUTPUT_FOLDER, "grayscale"
        )
        os.makedirs(grayscale_folder, exist_ok=True)

        cv2.imwrite(
            os.path.join(
                grayscale_folder,
                f"page_{page_number}.png"
            ),
            gray_image
        )

        # STEP 3: Apply inverted thresholding
        _, binary_image = cv2.threshold(
            gray_image,
            127,
            255,
            cv2.THRESH_BINARY_INV
        )

        # STEP 4: Find contours
        contours, hierarchy = cv2.findContours(
            binary_image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        print("Contours detected:", len(contours))

        # STEP 5: Draw filtered bounding rectangles
        box_image = original_image.copy()

        valid_regions = []

        for contour in contours:

            x, y, w, h = cv2.boundingRect(contour)

            if w > 100 and h > 100:
                valid_regions.append((x, y, w, h))

                cv2.rectangle(
                    box_image,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

        box_folder = os.path.join(
            OUTPUT_FOLDER, "bounding_boxes"
        )
        os.makedirs(box_folder, exist_ok=True)

        cv2.imwrite(
            os.path.join(
                box_folder,
                f"page_{page_number}_boxes.png"
            ),
            box_image
        )

        # STEP 6: Crop drawing regions with margin
        crop_folder = os.path.join(
            OUTPUT_FOLDER, "cropped_drawings"
        )
        os.makedirs(crop_folder, exist_ok=True)

        crop_count = 0
        margin = 120

        for x, y, w, h in valid_regions:

            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(original_image.shape[1], x + w + margin)
            y2 = min(original_image.shape[0], y + h + margin)

            cropped_image = original_image[y1:y2, x1:x2]

            crop_count += 1

            cv2.imwrite(
                os.path.join(
                    crop_folder,
                    f"page_{page_number}_drawing_{crop_count}.png"
                ),
                cropped_image
            )

        print("Bounding rectangles:", len(valid_regions))
        print("Drawing regions cropped:", crop_count)

    doc.close()

    print("\nAll PDF pages processed successfully!")


# MAIN PROGRAM
if __name__ == "__main__":

    pdf_path = "../uploads/sample.pdf"

    process_all_pages(pdf_path)
