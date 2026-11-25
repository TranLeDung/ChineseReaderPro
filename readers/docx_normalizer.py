import re
import pandas as pd

from docx import Document

from pypinyin import (
    pinyin,
    Style
)


def generate_pinyin(text):

    result = pinyin(
        text,
        style=Style.TONE
    )

    return " ".join(
        item[0]
        for item in result
    )


def contains_chinese(text):

    return bool(
        re.search(
            r'[\u4e00-\u9fff]',
            text
        )
    )


def normalize_docx(docx_file):

    document = Document(
        docx_file
    )

    rows = []

    row_id = 1

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if not text:
            continue

        if not contains_chinese(text):
            continue

        chinese = text

        rows.append({
            "ID": row_id,
            "Chinese": chinese,
            "Generated Pinyin":
                generate_pinyin(
                    chinese
                ),
            "Original Pinyin": "",
            "Meaning": ""
        })

        row_id += 1

    return pd.DataFrame(rows)