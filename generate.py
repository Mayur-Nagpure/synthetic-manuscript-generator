import os
import shutil
import random

from src.config import (
    WIDTH,
    HEIGHT,
    INPUT_DIR,
    FONT_DIR,
    OUTPUT_DIR,
    SCRIPTS,
    IMAGES_PER_SCRIPT,
    TRAIN_COUNT,
    VAL_COUNT,
)

from src.text_manager import (
    read_text,
    make_pages
)

from src.background import (
    create_background
)

from src.layout import (
    get_layout
)

from src.renderer import (
    render_page
)


# Decides which dataset split the current image belongs t0
def get_split(index):

    if index <= TRAIN_COUNT:
        return "train"

    if index <= TRAIN_COUNT + VAL_COUNT:
        return "validation"

    return "test"


#Generates all manuscript images and ground-truth files for one script
def generate_script(
    script_name,
    settings
):

    print(
        f"\n=== {script_name} ==="
    )

    # Get the input text and font paths for this script
    text_path = os.path.join(
        INPUT_DIR,
        settings["text"]
    )

    font_path = os.path.join(
        FONT_DIR,
        settings["font"]
    )

    # Stop if the source text file is missing
    if not os.path.exists(
        text_path
    ):

        print(
            "Missing text:",
            text_path
        )

        return

    # Stop if the font is missing
    if not os.path.exists(
        font_path
    ):

        print(
            "Missing font:",
            font_path
        )

        return

    # Read and clean the source manuscript text
    text = read_text(
        text_path
    )

    # Split the text into six lines for each generated image
    pages = make_pages(
        text,
        lines_per_page=6
    )

    print(
        "Unique manuscript pages:",
        len(pages)
    )

    # Make sure there is enough text for all requested images.
    if len(pages) < IMAGES_PER_SCRIPT:

        print(
            "ERROR: Not enough source text "
            "for 100 unique images."
        )

        print(
            "Need at least 600 wrapped lines."
        )

        return

    # Generate the requested number of images.
    for index in range(
        1,
        IMAGES_PER_SCRIPT + 1
    ):

        print(
            f"{script_name}: "
            f"{index}/{IMAGES_PER_SCRIPT}"
        )

        # Use a fixed seed for each image so its random
        # appearance can be reproduced later.
        random.seed(
            index
            * 7919
            + len(script_name)
        )

        page_lines = pages[
            index - 1
        ]

        # Create a fresh aged-paper background.
        background = create_background(
            WIDTH,
            HEIGHT
        )

        # Select a font size and line spacing that fit the page.
        font, line_height = get_layout(
            page_lines,
            font_path,
            WIDTH,
            HEIGHT
        )

        # Draw the manuscript text onto the background.
        image = render_page(
            background,
            page_lines,
            font,
            line_height
        )

        # Decide whether this image goes to train,
        # validation, or test.
        split = get_split(
            index
        )

        folder = os.path.join(
            OUTPUT_DIR,
            script_name,
            split
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        image_name = (
            f"Image_{index}.png"
        )

        md_name = (
            f"Image_{index}.md"
        )

        image_path = os.path.join(
            folder,
            image_name
        )

        md_path = os.path.join(
            folder,
            md_name
        )

        # Save the generated manuscript image.
        image.save(
            image_path,
            "PNG"
        )

        # Save the exact text used for this image as ground truth
        with open(
            md_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "\n".join(
                    page_lines
                )
            )

    print(
        f"Completed {script_name}"
    )


# Starts the complete generation process for all scripts
def main():

    print(
        "=" * 60
    )

    print(
        "SYNTHETIC MANUSCRIPT GENERATOR"
    )

    print(
        "100 IMAGES × 3 SCRIPTS"
    )

    print(
        "=" * 60
    )

    # Remove the previous output so every run starts clean
    if os.path.exists(
        OUTPUT_DIR
    ):

        shutil.rmtree(
            OUTPUT_DIR
        )

    os.makedirs(
        OUTPUT_DIR
    )

    # Generate the dataset for each configured script
    for script_name, settings in SCRIPTS.items():

        generate_script(
            script_name,
            settings
        )

    print(
        "\n"
        + "=" * 60
    )

    print(
        "DONE"
    )

    print(
        "300 manuscript images generated."
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":
    main()