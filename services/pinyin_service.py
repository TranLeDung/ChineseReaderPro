from pypinyin import (
    pinyin,
    Style
)


def get_pinyin(text):

    result = []

    for char in text:

        if char in "，。！？；：,.!?":

            result.append(char)

        else:

            py = pinyin(
                char,
                style=Style.TONE,
                strict=False
            )

            if py:

                result.append(
                    py[0][0]
                )

    return " ".join(result)