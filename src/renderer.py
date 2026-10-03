import random
from .handwriting import make_handwritten_line


# Places all generated text lines neatly inside the manuscript page
def render_page(background, lines, font, line_height):

    img = background.convert("RGBA")
    W, H = img.size

    # Reduce line spacing if needed so all lines stay inside the page
    line_height = min(
        line_height,
        int((H - 60) / len(lines))
    )

    # Center the block of text with a small random vertical shift
    total = len(lines) * line_height
    y0 = (H - total) // 2 - random.randint(2, 8)

    # A few lines may use slightly reddish ink
    n = random.choice([0, 0, 1, 1, 1, 2])

    reds = set(
        random.sample(
            range(len(lines)),
            min(n, len(lines))
        )
    )

    # Keep text away from the RIGHT-SIDE thread
    TEXT_LEFT = 35
    TEXT_RIGHT = W - 120

    text_width = TEXT_RIGHT - TEXT_LEFT

    for i, text in enumerate(lines):

        # Render the complete line with small handwriting variations
        layer = make_handwritten_line(
            text,
            font,
            i in reds
        )

        w, h = layer.size

        # Center each line with a very small random horizontal shift
        x = (
            TEXT_LEFT
            + (text_width - w) // 2
            + random.randint(-5, 5)
        )

        # Give each line a tiny vertical variation
        y = (
            y0
            + i * line_height
            + random.randint(-2, 2)
        )

        # Never allow text into the thread area.
        x = max(
            TEXT_LEFT,
            min(x, TEXT_RIGHT - w)
        )

        # Keep the text inside the top and bottom page boundaries
        y = max(
            20,
            min(y, H - h - 20)
        )

        # Add the handwritten line to the manuscript page
        img.alpha_composite(
            layer,
            (int(x), int(y))
        )

    return img.convert("RGB")