import fitz

from services.chinese_cleaner import (
    keep_chinese_only
)


def read_pdf(file):

    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    all_text = []

    for page in pdf:

        text = page.get_text()
        
        all_text.append(text)

    raw_text = "\n".join(
        all_text
    )

    clean_text = keep_chinese_only(
        raw_text
    )

    return clean_text