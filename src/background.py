import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


# Creates uneven shapes used for stain and other paper marks
def organic_shape(cx, cy, rx, ry, count=45):
    points = []

    for i in range(count):
        angle = 2 * np.pi * i / count
        radius = random.uniform(0.70, 1.30)

        points.append((
            cx + np.cos(angle) * rx * radius,
            cy + np.sin(angle) * ry * radius
        ))

    return points


# Adds large soft color variations so the paper does not look flat
def add_broad_aging(image, width, height):
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for _ in range(random.randint(14, 22)):
        cx = random.randint(-80, width + 80)
        cy = random.randint(-50, height + 50)
        rx = random.randint(50, 190)
        ry = random.randint(30, 125)
        opacity = random.randint(10, 38)

        color = random.choice([
            (95, 55, 24, opacity),
            (115, 66, 27, opacity),
            (135, 76, 30, opacity),
            (75, 48, 25, opacity),
            (150, 92, 40, opacity)
        ])

        draw.polygon(
            organic_shape(cx, cy, rx, ry),
            fill=color
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(random.uniform(12, 25))
    )

    return Image.alpha_composite(
        image.convert("RGBA"), layer
    )


#Adds faded liquid marks similar to old water or coffee stains
def add_dried_liquid_stains(image, width, height):
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for _ in range(random.randint(6, 11)):
        cx = random.randint(20, width - 20)
        cy = random.randint(20, height - 20)
        rx = random.randint(30, 120)
        ry = random.randint(18, 80)

        if random.random() < 0.35:
            color = random.choice([
                (70, 42, 21, 45),
                (83, 45, 20, 50),
                (100, 52, 20, 42)
            ])
        else:
            color = random.choice([
                (105, 60, 25, 20),
                (120, 70, 28, 25),
                (145, 85, 32, 18)
            ])

        draw.polygon(
            organic_shape(cx, cy, rx, ry),
            fill=color
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(random.uniform(5, 13))
    )

    return Image.alpha_composite(image, layer)


# Adds subtle edges around some stains to make them looknaturally dried
def add_stain_boundaries(image, width, height):
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for _ in range(random.randint(5, 10)):
        shape = organic_shape(
            random.randint(0, width),
            random.randint(0, height),
            random.randint(45, 160),
            random.randint(25, 95)
        )

        draw.line(
            shape + [shape[0]],
            fill=random.choice([
                (90, 50, 22, 20),
                (105, 58, 25, 25),
                (120, 68, 28, 18)
            ]),
            width=random.randint(2, 5)
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(random.uniform(2, 5))
    )

    return Image.alpha_composite(image, layer)


# Adjusts the paper colors to give it an older warmer appearance
def add_ancient_color(image, width, height):
    arr = np.asarray(
        image.convert("RGB")
    ).astype(np.float32)

    arr[:, :, 0] *= random.uniform(0.91, 0.96)
    arr[:, :, 1] *= random.uniform(0.86, 0.92)
    arr[:, :, 2] *= random.uniform(0.72, 0.82)

    yy, xx = np.mgrid[0:height, 0:width]

    variation = (
        3.0 * np.sin(xx / 170)
        + 2.0 * np.sin(yy / 125)
        + 1.5 * np.sin((xx + yy) / 250)
    )

    arr[:, :, 0] += variation
    arr[:, :, 1] += variation * 0.8
    arr[:, :, 2] += variation * 0.55

    return Image.fromarray(
        np.clip(arr, 0, 255).astype(np.uint8),
        "RGB"
    )


# Adds small random variations to imitate the texture of old paper
def add_paper_grain(image, width, height):
    arr = np.asarray(
        image.convert("RGB")
    ).astype(np.float32)

    noise = np.random.normal(
        0,
        random.uniform(2.0, 4.0),
        (height, width, 1)
    )

    arr += noise

    return Image.fromarray(
        np.clip(arr, 0, 255).astype(np.uint8),
        "RGB"
    )


# Creates uneven darkening and wear around the edges of the page.
def add_edge_wear(image, width, height):
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for _ in range(random.randint(35, 60)):
        side = random.choice([
            "top", "bottom", "left", "right"
        ])

        if side == "top":
            x = random.randint(-10, width + 10)
            y = random.randint(0, 28)

        elif side == "bottom":
            x = random.randint(-10, width + 10)
            y = random.randint(height - 28, height)

        elif side == "left":
            x = random.randint(0, 28)
            y = random.randint(-10, height + 10)

        else:
            x = random.randint(width - 28, width)
            y = random.randint(-10, height + 10)

        shape = organic_shape(
            x, y,
            random.randint(5, 24),
            random.randint(3, 18),
            20
        )

        draw.polygon(
            shape,
            fill=random.choice([
                (55, 32, 17, 40),
                (70, 37, 18, 50),
                (85, 43, 19, 45),
                (105, 55, 22, 35)
            ])
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(random.uniform(3, 6))
    )

    return Image.alpha_composite(
        image.convert("RGBA"), layer
    )


# Adds small irregular damage to a few corners of the page.
def add_torn_corners(image, width, height):
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    corners = [
        (0, 0),
        (width, 0),
        (0, height),
        (width, height)
    ]

    selected = random.sample(
        corners,
        random.randint(1, 3)
    )

    for cx, cy in selected:
        for _ in range(random.randint(3, 6)):
            rx = random.randint(10, 42)
            ry = random.randint(8, 38)

            x = (
                random.randint(0, rx)
                if cx == 0
                else random.randint(width - rx, width)
            )

            y = (
                random.randint(0, ry)
                if cy == 0
                else random.randint(height - ry, height)
            )

            draw.polygon(
                organic_shape(x, y, rx, ry, 18),
                fill=random.choice([
                    (52, 31, 17, 55),
                    (70, 36, 17, 65),
                    (88, 43, 19, 50)
                ])
            )

    layer = layer.filter(
        ImageFilter.GaussianBlur(2.5)
    )

    return Image.alpha_composite(
        image.convert("RGBA"), layer
    )


# Adds the old reddish thread mark along the right side.
# It is kept away from the writing area by the renderer.
def add_thread_stain(image, width, height):
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Keep the thread close to the right edge.
    x = random.randint(width - 75, width - 38)
    stain_x = x + random.randint(-4, 4)

    # Faded color left around the old thread.
    for offset in [-7, -4, 4, 7]:
        points = []

        for y in range(15, height - 15, 12):
            points.append((
                stain_x
                + offset
                + random.uniform(-2.5, 2.5),
                y
            ))

        draw.line(
            points,
            fill=(
                120,
                57,
                38,
                random.randint(25, 55)
            ),
            width=random.randint(2, 5)
        )

    # Two slightly irregular thread lines.
    for thread_offset in [-2, 3]:
        points = []

        for y in range(10, height - 10, 8):
            points.append((
                x
                + thread_offset
                + np.sin(y / 27)
                * random.uniform(0.5, 1.5)
                + random.uniform(-0.8, 0.8),
                y
            ))

        for i in range(len(points) - 1):
            if random.random() < 0.12:
                continue

            draw.line(
                (points[i], points[i + 1]),
                fill=random.choice([
                    (125, 49, 40, 85),
                    (140, 55, 42, 70),
                    (105, 48, 38, 60)
                ]),
                width=random.choice([1, 1, 2])
            )

    # Small marks where the thread appears to have pressed against the paper.
    for _ in range(random.randint(6, 12)):
        y = random.randint(20, height - 20)

        draw.ellipse(
            (
                x - random.randint(5, 10),
                y - random.randint(3, 8),
                x + random.randint(5, 10),
                y + random.randint(3, 8)
            ),
            fill=(
                120,
                50,
                35,
                random.randint(15, 45)
            )
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(
            random.uniform(0.3, 0.8)
        )
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        layer
    )


# Builds one complete aged-paper background by applying all effects
def create_background(width=1000, height=600):

    # Start with a warm parchment base.
    base = np.zeros(
        (height, width, 3),
        dtype=np.float32
    )

    base[:, :, :] = [201, 169, 115]

    # A little variation keeps the base from looking completely flat
    base += np.random.normal(
        0,
        3.0,
        (height, width, 1)
    )

    image = Image.fromarray(
        np.clip(
            base,
            0,
            255
        ).astype(np.uint8),
        "RGB"
    )

    # Apply the paper effects one after another
    image = add_broad_aging(
        image, width, height
    )

    image = add_dried_liquid_stains(
        image, width, height
    )

    image = add_stain_boundaries(
        image, width, height
    )

    image = add_ancient_color(
        image, width, height
    )

    image = add_paper_grain(
        image, width, height
    )

    image = add_edge_wear(
        image, width, height
    )

    image = add_torn_corners(
        image, width, height
    )

    # Thread is intentionally placed only on the right.
    image = add_thread_stain(
        image, width, height
    )

    return image.convert("RGB")