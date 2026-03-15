# Fluorescent Germ Analysis Tool 🦠✨

**The Goal:** This project was built to scientifically **test the efficiency of different cleaning wipes**. By measuring "germ" removal, we can prove which wipes actually work best and which ones just spread the mess around.

Built with **Python** and the **OpenCV** computer vision library.

## 🚀 How it Works

1.  **The "Blue Channel" Secret (Better than Grayscale!):** 
    Most computer vision projects just turn images into black and white (grayscale). But for this experiment, grayscale is too noisy because the camera's "auto-exposure" makes the whole table look bright! 

    Since fluorescent powder glows specifically in the blue/UV spectrum, we use a **Blue Channel Extraction** technique. This acts like "digital magic glasses" that only see blue light—making the germs pop with high contrast while making the background table virtually disappear. This ensures our "Germ Score" is accurate and not just counting reflections from the table.

2.  **Thresholding:** The computer highlights only the brightest blue pixels, turning them pure white on a black background.
3.  **Pixel Counting:** The program counts every white pixel (a germ) to give you a precise "Germ Score."

## 🛠️ Setup
... (rest of the file) ...

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
    *Or if using `uv`:*
    ```bash
    uv run code.py
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

## 🌟 Acknowledgements

This project was developed for a **Science Alliance** project by **Zahra Anwar** at Hidden Hills Elementary. You can learn more about the Science Alliance program [here](https://srvef.org/science-alliance/).

While the code was authored by **Zubair Anwar**, the core scientific methodology and logic were conceived and directed by **Zahra Anwar**, including:
*   **Blue Channel Extraction:** Identifying that isolating the blue/UV spectrum would best highlight fluorescent "germs".
*   **Precise Cropping:** The strategy to crop images before analysis to ignore background noise and focus on the testing surface.
*   **Normalization:** Developing the approach to normalize scores across different crop sizes to ensure fair scientific comparison.
