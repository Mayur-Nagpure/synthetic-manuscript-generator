from PIL import ImageFont


#Finds a font size that fits all lines inside the page
def get_layout(lines, font_path, width, height):

    #Try larger fonts first and reduce the size until everything fits
    for size in range(60, 34, -1):

        font = ImageFont.truetype(
            font_path,
            size
        )

        # Check the width of every line using the selected font
        widths = [
            font.getbbox(line)[2]
            - font.getbbox(line)[0]
            for line in lines
        ]

        # Keep enough vertical space between consecutive lines
        spacing = int(size * 1.17)

        # Use this font size only when both width and height fit
        if (
            max(widths) <= width - 100
            and len(lines) * spacing <= height - 55
        ):
            return font, spacing

    # Fallback size in case none of the larger sizes fit
    return (
        ImageFont.truetype(
            font_path,
            35
        ),
        42
    )