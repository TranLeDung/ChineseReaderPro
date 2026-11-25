from docx import Document


def read_docx(file):

    document = Document(file)

    result = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:

            result.append(text)

    return "\n".join(result)