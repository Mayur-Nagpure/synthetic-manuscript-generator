import re


#Reads the markdown file and removes the basic markdown formatting
def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove fenced code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.S)

    # Remove markdown heading symbols
    text = re.sub(r"^#+\s*", "", text, flags=re.M)

    # Remove bold formatting
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # Remove italic formatting
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # Convert line breaks and extra spaces into normal spaces
    text = text.replace("\r", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", " ", text)

    return text.strip()


#Groups words into lines without exceeding the character limit
def wrap_words(words, max_chars=43):
    lines = []
    current = ""

    for word in words:
        test = (
            word
            if not current
            else current + " " + word
        )

        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


#Splits the wrapped text into separate manuscript pages
def make_pages(text, lines_per_page=6):
    words = text.split()

    all_lines = wrap_words(
        words,
        max_chars=43
    )

    pages = []

    for i in range(
        0,
        len(all_lines),
        lines_per_page
    ):
        page_lines = all_lines[
            i:i + lines_per_page
        ]

        if page_lines:
            pages.append(page_lines)

    return pages