# Fluorescent Germ Analysis Tool 🦠✨

This project is a scientific utility designed to measure "germ" removal for science experiments. It uses computer vision to analyze photos of surfaces treated with fluorescent powder (glowing germs) under a blacklight.

By isolating the **Blue Channel** of a digital image, the program can precisely count how much of a surface is "covered in germs" before and after cleaning.

## 🚀 How it Works

1.  **Blue Channel Extraction:** Since fluorescent powder glows in the blue/UV spectrum, we wear "digital magic glasses" that only see blue light, making the germs stand out while making the table/background disappear.
2.  **Thresholding:** The computer highlights only the brightest blue pixels, turning them pure white on a black background.
3.  **Pixel Counting:** The program counts every white pixel (a germ) to give you a precise "Germ Score."

## 🛠️ Setup

### Prerequisites
*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

### Installation
1.  Clone or download this repository.
2.  Install the required dependencies:
    ```bash
    pip install opencv-python numpy
    ```
    *Or if using `uv`:*
    ```bash
    uv sync
    ```

## 📸 Running the Analysis

1.  Place your "Before" and "After" photos in a folder (e.g., `run1/`).
2.  Run the analysis script:
    ```bash
    python code.py
    ```
3.  Follow the prompts:
    *   **Folder path:** Enter the path to your photos.
    *   **Crop:** Choose 'y' to ignore the edges of the table and focus on the center.
    *   **Percentage:** Choose 'y' to see scores as coverage percentages (useful for comparisons).
    *   **Threshold:** Use the default `150` or adjust if your photos are very bright or very dim.
    *   **Save Proof:** Choose 'y' to generate an `analysis_results` folder containing the black-and-white "maps" for your project board.

## 📊 Calculating Your Results

After the program gives you the **Before Score** and **After Score**, use this formula to find your final answer:

**Percent Removed = ((Before Score - After Score) / Before Score) × 100**

---
*Developed for science enthusiasts and future researchers.*
