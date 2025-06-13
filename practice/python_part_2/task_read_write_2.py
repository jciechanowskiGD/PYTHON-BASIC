"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words

def save(words,files,encodings):
    for f_encoding in zip(files,encodings):
        with open(f_encoding[0], "w", encoding=f_encoding[1]) as f:
            f.write("\n".join(words))

if __name__ == "__main__":
    words = generate_words()
    save(words,('file1.txt','file2.txt'),('utf-8','cp1252'))
