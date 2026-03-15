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

### 1. File Naming Convention
To automatically pair "Before" and "After" data, your photos must follow this naming format:
`run{N}_{wipe}_{before|after}.png`

**Example:**
*   `run1_clorox_before.png`
*   `run1_clorox_after.png`

### 2. Execution
1.  Place your photos in a folder (e.g., `run1/`).
2.  Run the analysis script:
    ```bash
    python code.py
    ```
    *Or if using `uv`:*
    ```bash
    uv run code.py
    ```
3.  Follow the prompts for cropping and thresholding.

### 3. Understanding the Output
The program will generate a scientific table pairing your results:

```text
Run  | Wipe            | before_germ_count | before_total_pixels | before_percent_lit | after_germ_count | after_total_pixels | after_percent_lit
-------------------------------------------------------------------------------------------------------------------------------------------------------
1    | clorox          | 275587            | 5068800             | 5.44%              | 523708           | 4687500            | 11.17%           
1    | great_value     | 725272            | 4753152             | 15.26%             | 246595           | 4583904            | 5.38%            
```

## 📊 Calculating Your Results

After the program gives you the **before_percent_lit** and **after_percent_lit**, use this formula to find your final answer:

**Percent Removed = ((before_percent_lit - after_percent_lit) / before_percent_lit) × 100**

---
*Developed for science enthusiasts and future researchers.*

## 🌟 Acknowledgements

This project was developed for a **Science Alliance** project by **Zahra Anwar** at Hidden Hills Elementary. You can learn more about the Science Alliance program [here](https://srvef.org/science-alliance/).

While the code was authored by **Zubair Anwar**, the core scientific methodology and logic were conceived and directed by **Zahra Anwar**, including:
*   **Blue Channel Extraction:** Identifying that isolating the blue/UV spectrum would best highlight fluorescent "germs".
*   **Precise Cropping:** The strategy to crop images before analysis to ignore background noise and focus on the testing surface.
*   **Normalization:** Developing the approach to normalize scores across different crop sizes to ensure fair scientific comparison.
