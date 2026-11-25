import re


def split_sentences(text):

    # Ưu tiên tách theo xuống dòng trước

    lines = text.splitlines()

    sentences = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        sentences.append(line)

    return sentences