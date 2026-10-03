import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


# Dark ink colors used for normal handwritten text
BLACK = [
    (30, 27, 22),
    (40, 31, 22),
    (48, 34, 22),
    (55, 38, 24)
]

# Slightly reddish ink colors for occasional variation
RED = [
    (125, 50, 37),
    (140, 56, 40),
    (115, 46, 34)
]


# Renders one line of text with small natural handwriting variations
def make_handwritten_line(text, font, red=False):
    box = font.getbbox(text)
    w, h = box[2] - box[0], box[3] - box[1]
    p = 24

    # Extra space around the text is needed for the small distortions
    img = Image.new(
        "RGBA",
        (w + 2 * p, h + 2 * p),
        (0, 0, 0, 0)
    )

    ink = random.choice(
        RED if red else BLACK
    )

    alpha = random.randint(
        190 if red else 215,
        245
    )

    d = ImageDraw.Draw(img)

    # Sometimes add a very faint offset stroke to imitate ink spread
    if random.random() < .6:
        d.text(
            (p + 1, p + 1),
            text,
            font=font,
            fill=(*ink, random.randint(18, 35))
        )

    # Main text stroke.
    d.text(
        (p, p),
        text,
        font=font,
        fill=(*ink, alpha)
    )

    # Convert the image into an array so the whole line can be warped
    a = np.array(img)

    H, W = a.shape[:2]
    yy, xx = np.mgrid[:H, :W]

    # Small vertical movement gives the writing a natural uneven baseline
    dy = (
        random.uniform(.7, 1.5) * np.sin(
            xx / random.uniform(38, 58)
        )
        +
        random.uniform(.2, .7) * np.sin(
            xx / random.uniform(80, 125)
        )
    )

    # Adds a very small horizontal variation
    dx = (
        random.uniform(.15, .45)
        * np.sin(yy / random.uniform(25, 40))
    )

    sy = np.clip(
        (yy - dy).astype(int),
        0,
        H - 1
    )

    sx = np.clip(
        (xx - dx).astype(int),
        0,
        W - 1
    )

    # Apply the distortion to the complete line
    # This keeps Indic characters and their marks together
    img = Image.fromarray(
        a[sy, sx].astype("uint8"),
        "RGBA"
    )

    # Randomly apply a small amount of blur to imitate old ink
    r = random.random()

    if r < .12:
        img = img.filter(
            ImageFilter.GaussianBlur(
                random.uniform(.25, .45)
            )
        )

    elif r < .35:
        img = img.filter(
            ImageFilter.GaussianBlur(
                random.uniform(.06, .16)
            )
        )

    # A very small rotation makes each line slightly different
    return img.rotate(
        random.uniform(-.22, .22),
        Image.Resampling.BICUBIC,
        expand=True
    )