"""
Fluorescent Germ Analysis Tool

Developed for a Science Alliance project by Zahra Anwar (Hidden Hills Elementary).
Science Alliance: https://srvef.org/science-alliance/

Scientific Methodology & Logic: Zahra Anwar
- Blue Channel Extraction for fluorescent detection
- Region of Interest (ROI) cropping strategies
- Data normalization for scientific comparison

Code Implementation: Zubair Anwar
"""

import cv2
import numpy as np
import os
import re

def get_final_science_data(image_path, crop=True, threshold=150, save_dir=None):
    """
    Processes a single image to detect fluorescent 'germ' markers using Blue Channel Extraction.
    
    This function targets the specific blue/ultraviolet glow emitted by fluorescent powders
    under a blacklight. By isolating the blue channel, we significantly reduce noise from 
    other light sources compared to standard grayscale conversion.

    Args:
        image_path (str): Full path to the image file to analyze.
        crop (bool): If True, analyzes only the center 40% (30% to 70%) of the image. 
                    Useful for ignoring table edges or background clutter.
        threshold (int): The brightness cutoff (0-255). Pixels brighter than this 
                         in the blue channel are counted as 'germs'.
        save_dir (str, optional): Directory to save validation images (Blue channel & Binary Mask).

    Returns:
        tuple: (germ_count, total_pixels)
               - germ_count: Number of pixels meeting the threshold.
               - total_pixels: Total number of pixels analyzed (depends on crop).
    """
    # Load the image using OpenCV (BGR format)
    img = cv2.imread(image_path)
    if img is None:
        return 0, 0

    # 1. STANDARDIZE THE REGION OF INTEREST (ROI)
    # We crop to the center of the image to ensure we are looking at the 
    # testing surface and not the surrounding environment.
    height, width, _ = img.shape
    if crop:
        start_row, end_row = int(height * 0.3), int(height * 0.7)
        start_col, end_col = int(width * 0.3), int(width * 0.7)
        roi = img[start_row:end_row, start_col:end_col]
    else:
        roi = img

    # 2. BLUE CHANNEL EXTRACTION
    # Fluorescent powder glows primarily in the blue/UV spectrum.
    # OpenCV loads images as (Blue, Green, Red). Channel 0 is BLUE.
    # Extracting only the blue channel makes the 'germs' stand out much more
    # than if we just converted the whole image to black and white (grayscale).
    blue_channel = roi[:, :, 0]

    # 3. APPLY THRESHOLD (The "Magic Highlighter")
    # This creates a 'Binary Mask'. Any pixel brighter than our threshold becomes 
    # pure white (255), and everything else becomes pure black (0).
    _, mask = cv2.threshold(blue_channel, threshold, 255, cv2.THRESH_BINARY)

    # 4. SAVE VALIDATION IMAGES (Proof of Analysis)
    # These images allow us to verify that the computer is 'seeing' the same
    # thing we are. The mask is your visual proof for your project board.
    if save_dir:
        base_name = os.path.basename(image_path)
        name, _ = os.path.splitext(base_name)
        # Save the Blue Channel view (shows what the computer is looking at)
        cv2.imwrite(os.path.join(save_dir, f"{name}_blue.jpg"), blue_channel)
        # Save the Binary Mask (shows what the computer counted)
        cv2.imwrite(os.path.join(save_dir, f"{name}_mask.jpg"), mask)

    # 5. CALCULATE RESULTS
    # Count how many pixels are white (non-zero) in our map.
    germ_count = np.count_nonzero(mask)
    total_pixels = mask.size

    return germ_count, total_pixels


def main():
    """
    Main execution loop for analyzing a folder of science project photos.
    Prompts the user for settings and displays a summary of 'germ scores'.
    """
    print("\n" + "="*50)
    print("      FLUORESCENT GERM ANALYSIS TOOL")
    print("      A Science Alliance Project by Zahra Anwar")
    print("="*50)

    # 1. Folder Selection
    photo_dir = input("\nEnter the folder path to analyze: ").strip()
    
    if not os.path.isdir(photo_dir):
        print(f"Error: The directory '{photo_dir}' does not exist.")
        return

    # 2. Configuration Settings
    crop_choice = input("Crop to center to avoid edge noise? (y/n): ").strip().lower()
    use_crop = crop_choice == 'y'

    threshold_input = input("Enter brightness threshold (0-255, default 150): ").strip()
    try:
        threshold = int(threshold_input) if threshold_input else 150
    except ValueError:
        print("Invalid threshold. Using default 150.")
        threshold = 150

    # 3. Setup Validation Directory
    save_val = input("Save 'Proof' images for your project board? (y/n): ").strip().lower()
    save_dir = None
    if save_val == 'y':
        save_dir = os.path.join(photo_dir, "analysis_results")
        os.makedirs(save_dir, exist_ok=True)
        print(f"\n[Info] Saving validation images to: {save_dir}")

    # 4. Group Files into (Run, Wipe) Pairs
    # Pattern: run{N}_{wipe}_{before|after}.{ext}
    data_pairs = {}
    for filename in os.listdir(photo_dir):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            # Regex to find run, wipe name, and condition (before/after)
            # We use (.+) for the wipe name to allow underscores like 'great_value'
            match = re.search(r"run(\d+)_(.+)_(before|after)", filename.lower())
            if match:
                run_num, wipe_name, condition = match.groups()
                key = (int(run_num), wipe_name)
                if key not in data_pairs:
                    data_pairs[key] = {}
                data_pairs[key][condition] = filename

    if not data_pairs:
        print("\nNo matching image pairs found! Please ensure your files follow the format:")
        print("run1_wipe_before.png, run1_wipe_after.png, etc.")
        return

    print(f"\nAnalyzing image pairs with Blue Channel Extraction (Threshold: {threshold})...")
    header = f"{'Run':<4} | {'Wipe':<15} | {'before_germ_count':<17} | {'before_total_pixels':<19} | {'before_percent_lit':<18} | {'after_germ_count':<16} | {'after_total_pixels':<18} | {'after_percent_lit'}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)

    # 5. Process and Display Results
    for (run, wipe), conditions in sorted(data_pairs.items()):
        # Process 'Before'
        b_score = b_total = b_pct = "N/A"
        if 'before' in conditions:
            score, total = get_final_science_data(
                os.path.join(photo_dir, conditions['before']), 
                crop=use_crop, threshold=threshold, save_dir=save_dir
            )
            b_score, b_total = score, total
            b_pct = f"{(score/total*100):.2f}%" if total > 0 else "0.00%"

        # Process 'After'
        a_score = a_total = a_pct = "N/A"
        if 'after' in conditions:
            score, total = get_final_science_data(
                os.path.join(photo_dir, conditions['after']), 
                crop=use_crop, threshold=threshold, save_dir=save_dir
            )
            a_score, a_total = score, total
            a_pct = f"{(score/total*100):.2f}%" if total > 0 else "0.00%"

        # Print combined row
        print(f"{run:<4} | {wipe:<15} | {str(b_score):<17} | {str(b_total):<19} | {b_pct:<18} | {str(a_score):<16} | {str(a_total):<18} | {a_pct}")

    print(separator)
    print("\nAnalysis complete!")
    print("Use the Before % and After % to calculate 'Percent Removed':")
    print("((Before_% - After_%) / Before_%) * 100")


if __name__ == "__main__":
    main()
