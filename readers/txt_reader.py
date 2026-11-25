def read_txt(file):

    try:
        return file.read().decode(
            "utf-8"
        )

    except:

        file.seek(0)

        return file.read().decode(
            "gb18030"
        )