from paddleocr import PaddleOCR

# Khởi tạo OCR 1 lần duy nhất

ocr = PaddleOCR(
    lang="ch"
)


def image_to_text(image_path):

    result = ocr.predict(
        image_path
    )

    texts = []

    for item in result:

        if "rec_texts" in item:

            texts.extend(
                item["rec_texts"]
            )

    return "\n".join(texts)