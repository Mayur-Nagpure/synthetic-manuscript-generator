# Synthetic Manuscript Generator

A Python pipeline for generating synthetic historical manuscript images for Devanagari, Modi, and Sharada scripts with matching OCR ground-truth annotations.

## What It Does

The pipeline takes raw Markdown text and:

- Creates an aged manuscript-style background.
- Adds stains, paper grain, edge wear, torn corners, and a right-side thread effect.
- Renders Indic text using the selected script font.
- Adds small handwriting variations such as waviness, slight rotation, ink variation, blur, and fading.
- Keeps text inside the page boundaries.
- Saves each generated image together with the exact text used to create it.

The current configuration generates **100 images per script**, with an **85/10/5 train-validation-test split**.

## Technologies Used

- Python 3
- Pillow - image creation, drawing, fonts, filters, and image processing
- NumPy - image arrays, noise, color variation, and text warping

## Project Structure

```text
synthetic-manuscript-generator/
│
├── data/
│   └── input/
│       ├── devanagari_md.md
│       ├── Modi_md.md
│       └── sharada_md.md
│
├── fonts/
│   ├── Devanagari.ttf
│   ├── Modi.ttf
│   └── Sharada.ttf
│
├── src/
│   ├── background.py
│   ├── config.py
│   ├── handwriting.py
│   ├── layout.py
│   ├── renderer.py
│   └── text_manager.py
│
├── generate.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How It Works

### 1. Text Processing

`text_manager.py` reads the Markdown files, removes basic Markdown formatting, wraps the text into lines, and creates groups of six lines for each image.

### 2. Background Generation

`background.py` creates the manuscript background.

It starts with a warm paper base and adds randomized:

- aging patches
- stains
- paper grain
- color variation
- edge wear
- torn corners
- right-side thread marks

### 3. Text Rendering

`handwriting.py` renders a complete text line using the selected font.

Small transformations are applied to the whole line, including:

- baseline waviness
- small horizontal movement
- ink color and opacity variation
- blur
- slight rotation

The whole line is transformed together so Indic character marks stay aligned.

### 4. Layout

`layout.py` checks the text width and height and selects a font size that fits the available page area.

### 5. Final Rendering

`renderer.py` places the generated text on the background, keeps it within the page boundaries, and leaves space for the right-side thread effect.

### 6. Dataset Generation

`generate.py` runs the complete pipeline for all configured scripts and saves:

```text
Image_1.png
Image_1.md
```

The `.md` file contains the exact text rendered in the corresponding image.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/synthetic-manuscript-generator.git
cd synthetic-manuscript-generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure the required fonts are in `fonts/` and the input Markdown files are in `data/input/`.

## Run

Run the complete generator:

```bash
python generate.py
```

The current configuration generates:

```text
Devanagari: 100 images
Modi:       100 images
Sharada:    100 images
Total:      300 images
```

Each script is split into:

```text
Train:       85
Validation:  10
Test:         5
```

## Output

```text
output/
├── devanagari/
│   ├── train/
│   ├── validation/
│   └── test/
├── modi/
│   ├── train/
│   ├── validation/
│   └── test/
└── sharada/
    ├── train/
    ├── validation/
    └── test/
```

Each image has a matching `.md` annotation file.

Example:

```text
Image_25.png
Image_25.md
```

## Configuration

Generation settings are in:

```text
src/config.py
```

Current settings:

```python
WIDTH = 1000
HEIGHT = 600

IMAGES_PER_SCRIPT = 100

TRAIN_COUNT = 85
VAL_COUNT = 10
TEST_COUNT = 5
```

Scripts and their fonts/input files can also be changed from `SCRIPTS` in `config.py`.

## Hugging Face Dataset

The generated dataset is hosted separately on Hugging Face with three script subsets/configurations:

```text
devanagari
modi
sharada
```

Dataset:

```text
[View Dataset on Hugging Face](https://huggingface.co/datasets/M3221/synthetic-manuscript-dataset)
```

Dataset link:

```text
[View Dataset on Hugging Face](https://huggingface.co/datasets/M3221/synthetic-manuscript-dataset)

https://huggingface.co/datasets/M3221/synthetic-manuscript-dataset/tree/main
```

## Author

Mayur Nagpure
