import json
import os

PROGRESS_FILE = "data/reading_progress.json"


def load_progress():

    if not os.path.exists(
        PROGRESS_FILE
    ):

        return {}

    with open(
        PROGRESS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_progress(data):

    with open(
        PROGRESS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )