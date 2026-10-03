# Synthetic Manuscript Generator

A Python pipeline for generating synthetic historical manuscript folios for Devanagari, Modi, and Sharada scripts with synchronized OCR ground-truth annotations.

## Assignment Overview

This project is an automated Python pipeline for generating realistic synthetic historical manuscript images from raw text.

The pipeline creates aged manuscript backgrounds, renders Indic text with handwriting-like variations, and generates a matching Markdown ground-truth file for every image.

The current pipeline supports:

- Devanagari
- Modi
- Sharada

The project is configurable, so additional scripts can be added by providing the required font and input text.

## Features

- Aged manuscript-style backgrounds
- Natural paper color variation
- Broad aging patches
- Dried liquid-like stains
- Irregular stain boundaries
- Paper grain
- Edge wear
- Damaged corners
- Reddish thread impression on the right side
- Natural ink color variation
- Slight handwriting waviness
- Small text alignment variation
- Slight text rotation
- Ink spreading and fading effects
- Text boundary protection
- Matching Markdown ground-truth files
- Train, validation, and test dataset splits
- Support for multiple Indic scripts

## Dataset

The generator creates:

- 100 Devanagari images
- 100 Modi images
- 100 Sharada images

Total:

```text
300 images