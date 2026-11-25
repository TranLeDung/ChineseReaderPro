import re


def keep_chinese_only(text):

    lines = text.splitlines()

    chinese_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        chinese = re.findall(
            r'[\u4e00-\u9fff，。！？；：、]+',
            line
        )

        if chinese:

            chinese_lines.append(
                "".join(chinese)
            )

    return "\n".join(
        chinese_lines
    )