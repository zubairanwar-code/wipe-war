# Fluorescent Germ Analysis Tool 🦠✨

**The Goal:** This project was built to scientifically **test the efficiency of different cleaning wipes**. By measuring "germ" removal, we can prove which wipes actually work best and which ones just spread the mess around.

Built with **Python**, the **OpenCV** computer vision library, and **Matplotlib**.

## 🚀 How it Works

1.  **The "Blue Channel" Secret (Better than Grayscale!):** 
    Most computer vision projects just turn images into black and white (grayscale). But for this experiment, grayscale is too noisy because the camera's "auto-exposure" makes the whole table look bright! 

    Since fluorescent powder glows specifically in the blue/UV spectrum, we use a **Blue Channel Extraction** technique. This acts like "digital magic glasses" that only see blue light—making the germs pop with high contrast while making the background table virtually disappear. This ensures our "Germ Score" is accurate and not just counting reflections from the table.

2.  **Thresholding:** The computer highlights only the brightest blue pixels, turning them pure white on a black background.
3.  **Pixel Counting:** The program counts every white pixel (a germ) to give you a precise "Germ Score."
4.  **Percent Removed Calculation:** The program automatically calculates the cleaning efficiency of each wipe using the scientific formula:
    $$\text{Percent Removed} = \frac{\text{Before\% Lit} - \text{After\% Lit}}{\text{Before\% Lit}} \times 100$$
    *Note: If the germ count increases after wiping, this represents a negative percentage (meaning germs were spread instead of cleaned).*

## 🛠️ Setup

### Prerequisites
*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

### Installation
1.  Clone or download this repository.
2.  Install the required dependencies:
    ```bash
    pip install opencv-python numpy matplotlib
    ```
    *Or if using `uv`:*
    ```bash
    uv sync
    ```

## 📸 Running the Analysis

### 1. File Naming Convention
To pair "Before" and "After" data, your photos should follow one of these naming formats:
*   `run{N}_{wipe}_{before|after}.jpg` (e.g., `run1_clorox_before.png`)
*   `{wipe}_{before|after}.jpg` (e.g., `clorox_before.jpg` — will default to Run 1, or infer the run number from the folder name if it contains "run{N}").

### 2. Execution

You can run the tool in two modes:

#### Option A: Command Line Mode (Automated)
Run the script passing the folder path as an argument. You can customize the threshold and cropping settings:
```bash
uv run code.py -d path/to/folder -t 150
```
**Available Arguments:**
*   `-d`, `--dir`: Folder containing photo pairs to analyze.
*   `-t`, `--threshold`: Brightness threshold cutoff (0-255, default 150).
*   `--no-crop`: Disable center cropping (analyzes the whole image).
*   `--crop-ratios`: Custom crop percentages: `y_start y_end x_start x_end` (0.0 to 1.0, default `0.3 0.7 0.3 0.7`).
*   `--no-val`: Disable saving validation images.
*   `--no-chart`: Disable generating the matplotlib comparison chart.

#### Option B: Interactive Mode (Prompt-guided)
Simply run the script with no arguments, and follow the interactive prompts:
```bash
uv run code.py
```

### 3. Visual Parameter Tuning (Tuner GUI)
Before running a batch analysis, you can use the interactive tuning tool to find the perfect brightness threshold and crop area visually:
```bash
uv run tune_threshold.py --image path/to/sample_image.jpg
```
This opens an OpenCV window with real-time sliders. Adjust the sliders to see:
*   **Original Image** with the green crop box overlay.
*   **Isolated Blue Channel** (what the computer sees).
*   **Binary Mask** (what the computer counts).

When you press `q` or `ESC` to exit, the script prints the exact Python arguments to use in `code.py`.

### 4. Understanding the Output
The program generates a results directory called `analysis_results/` inside your photo folder, containing:
1.  **Results Table (Console):** A summary printed in your terminal.
2.  **`results_summary.md`:** A polished Markdown report table.
3.  **`results_summary.csv`:** A CSV spreadsheet of results, suitable for import into Excel or Google Sheets.
4.  **`cleaning_efficiency_comparison.png`:** A beautiful bar chart visualizing the comparison (green for cleaning, red for spreading).
5.  **Validation Proofs (optional):** Extracted `*_blue.jpg` and `*_mask.jpg` images for each photo, serving as visual proof for your project board.

---
*Developed for science enthusiasts and future researchers.*

## 🌟 Acknowledgements

This project was developed for a **Science Alliance** project by **Zahra Anwar** at Hidden Hills Elementary. You can learn more about the Science Alliance program [here](https://srvef.org/science-alliance/).

While the code was authored by **Zubair Anwar**, the core scientific methodology and logic were conceived and directed by **Zahra Anwar**, including:
*   **Blue Channel Extraction:** Identifying that isolating the blue/UV spectrum would best highlight fluorescent "germs".
*   **Precise Cropping:** The strategy to crop images before analysis to ignore background noise and focus on the testing surface.
*   **Normalization:** Developing the approach to normalize scores across different crop sizes to ensure fair scientific comparison.
