# Code Review and Improvement Plan 🦠✨

We have conducted a review of the Fluorescent Germ Analysis Tool codebase. Below is an analysis of the current code, its limitations, and a plan for implementing state-of-the-art improvements that will make the tool more robust, user-friendly, and scientifically powerful.

---

## 🔍 Code Review & Limitations

### 1. Analysis Logic & Precision (`code.py` & `main.py`)
*   **Duplicate Implementations**: `main.py` uses grayscale conversion (`cv2.COLOR_BGR2GRAY`), whereas `code.py` uses Blue Channel Extraction (`roi[:, :, 0]`). The latter is scientifically superior for fluorescent detection under UV light (as documented in `README.md` and `explanation.md`). However, having two distinct main files with different logics is confusing.
*   **Lack of Automatic Efficiency Calculation**: The core scientific goal is to calculate the **Percent Removed** for each wipe:
    $$\text{Percent Removed} = \frac{\text{Before\%} - \text{After\%}}{\text{Before\%}} \times 100$$
    Currently, the scripts output the percentages but leave the math to the user. The program should calculate this automatically and include it in the output table.
*   **Negative Efficiency Handling**: In some runs (e.g., Clorox run 1), the germ count *increases* after wiping (meaning the wipe spread the contamination instead of cleaning it). The script should handle this gracefully and display it (e.g. as a negative removal percentage or with a warning).

### 2. Usability & Interactivity
*   **Blind Thresholding**: Choosing a brightness threshold (e.g. 150) is done blindly. The user cannot see what the computer is actually counting without running the script, saving the validation images, and opening them manually.
*   **Strict Naming Pattern**: The regex `run(\d+)_(.+)_(before|after)` fails if images do not contain the `run{N}_` prefix in their names (which is the case for files directly in `images/run1/` like `clorox_before.jpg`).
*   **No Command-Line Arguments**: The CLI is purely interactive. This makes automation, batch processing, or running tests tedious.
*   **No Persistent Data Reports**: Results are only printed to the terminal console. They are not saved as a CSV or Markdown report file for easy sharing or embedding in papers/slides.
*   **No Visualizations**: A science fair project is much more impactful with data visualizations. Currently, there is no automatic charting.

---

## 🛠️ Proposed Improvements

We propose the following enhancement plan:

### Phase 1: Robust File Handling & Automated Metrics
1.  **Flexible Regex Matching**: Update file grouping to support optional run prefixes. If the run prefix is missing, automatically infer it from the directory path (e.g., if path contains `run1`, set run to 1; otherwise default to 1).
2.  **Calculate Percent Removed**: Compute and display the clean score improvement directly in the terminal output. Handle negative percentages (meaning contamination increased/spread) and division-by-zero errors.

### Phase 2: Professional Reporting & Visualization
1.  **CSV and Markdown Reports**: Automatically save a `results_summary.csv` and a polished `results_summary.md` inside the output directory.
2.  **Automated Charting (`matplotlib`)**: Add `matplotlib` to `pyproject.toml`. Generate a beautiful, publication-ready bar chart (`cleaning_efficiency_comparison.png`) showing the cleaning efficiency of each wipe, colored by performance.

### Phase 3: Developer & Automation Enhancements
1.  **Command-Line Arguments (`argparse`)**: Allow passing `--dir`, `--threshold`, `--no-crop`, `--no-val`, and `--chart` as CLI arguments. If arguments are provided, bypass interactive prompts for automated running.
2.  **Unify Entrypoints**: Refactor `main.py` to act as a clean wrapper that invokes the optimized `code.py` logic, maintaining backward compatibility while avoiding duplicate code paths.

### Phase 4: Interactive Visual Tuning GUI (`tune_threshold.py`)
1.  **Visual Parameter Tuner**: Create a new script, [tune_threshold.py](file:///Users/zubairanwar/code/wipe-war/tune_threshold.py), using OpenCV's GUI capabilities.
2.  **Real-Time Sliders**:
    *   **Threshold Slider** (0-255)
    *   **Crop Sliders** (top, bottom, left, right percentages)
3.  **Side-by-Side Views**: Show the original image (with crop box overlaid), the isolated blue channel, and the binary mask in real-time as the sliders move.

---

## 📋 Implementation Tasks

- [ ] **Task 1**: Update `pyproject.toml` to include `matplotlib`.
- [ ] **Task 2**: Refactor `code.py` to:
  *   Accept command-line arguments via `argparse`.
  *   Use a flexible naming regex and infer run number if missing.
  *   Calculate "Percent Removed" directly.
  *   Save results to CSV and Markdown tables.
  *   Generate a comparison bar chart if `matplotlib` is installed.
- [ ] **Task 3**: Create `tune_threshold.py` for visual threshold/crop tuning.
- [ ] **Task 4**: Make `main.py` call the unified implementation in `code.py`.
- [ ] **Task 5**: Update `README.md` to document the new features.
- [ ] **Task 6**: Run a verification test to ensure everything works end-to-end.
