"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

import os


def extract_vals(directory: str):
    files = os.listdir(directory)
    vals = []

    for filename in files:
        with open(f"{directory}/{filename}") as f:
            vals.append(f.read())

    return vals


if __name__ == "__main__":
    with open("result.txt", "w") as f:
        f.write(",".join(extract_vals("./files")))
