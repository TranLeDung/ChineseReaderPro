from ebooklib import epub
from bs4 import BeautifulSoup


def read_epub(file):

    book = epub.read_epub(file)

    text_parts = []

    for item in book.get_items():

        if item.get_type() == 9:

            soup = BeautifulSoup(
                item.get_content(),
                "html.parser"
            )

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            if text:

                text_parts.append(text)

    return "\n".join(text_parts)