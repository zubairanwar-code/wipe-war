"""
Fluorescent Germ Analysis Tool

Developed for a Science Alliance project by Zahra Anwar (Hidden Hills Elementary).
Science Alliance: https://srvef.org/science-alliance/

Scientific Methodology & Logic: Zahra Anwar
- Blue Channel Extraction for fluorescent detection
- Region of Interest (ROI) cropping strategies
- Data normalization for scientific comparison

Code Implementation: Zubair Anwar & AI Assistant
"""

import cv2
import numpy as np
import os
import re
import argparse
import sys

def get_final_science_data(image_path, crop=True, threshold=150, save_dir=None, crop_ratios=(0.3, 0.7, 0.3, 0.7)):
    """
    Processes a single image to detect fluorescent 'germ' markers using Blue Channel Extraction.
    
    This function targets the specific blue/ultraviolet glow emitted by fluorescent powders
    under a blacklight. By isolating the blue channel, we significantly reduce noise from 
    other light sources compared to standard grayscale conversion.

    Args:
        image_path (str): Full path to the image file to analyze.
        crop (bool): If True, analyzes only a sub-rectangle of the image. 
        threshold (int): The brightness cutoff (0-255). Pixels brighter than this 
                         in the blue channel are counted as 'germs'.
        save_dir (str, optional): Directory to save validation images (Blue channel & Binary Mask).
        crop_ratios (tuple): Y-start, Y-end, X-start, X-end float percentages (0.0 to 1.0).

    Returns:
        tuple: (germ_count, total_pixels)
               - germ_count: Number of pixels meeting the threshold.
               - total_pixels: Total number of pixels analyzed (depends on crop).
    """
    # Load the image using OpenCV (BGR format)
    img = cv2.imread(image_path)
    if img is None:
        print(f"[Warning] Could not read image at: {image_path}")
        return 0, 0

    # 1. STANDARDIZE THE REGION OF INTEREST (ROI)
    # We crop to the center of the image to ensure we are looking at the 
    # testing surface and not the surrounding environment.
    height, width, _ = img.shape
    if crop:
        y_start, y_end, x_start, x_end = crop_ratios
        start_row, end_row = int(height * y_start), int(height * y_end)
        start_col, end_col = int(width * x_start), int(width * x_end)
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
        name, ext = os.path.splitext(base_name)
        # Save the Blue Channel view (shows what the computer is looking at)
        cv2.imwrite(os.path.join(save_dir, f"{name}_blue.jpg"), blue_channel)
        # Save the Binary Mask (shows what the computer counted)
        cv2.imwrite(os.path.join(save_dir, f"{name}_mask.jpg"), mask)

    # 5. CALCULATE RESULTS
    # Count how many pixels are white (non-zero) in our map.
    germ_count = np.count_nonzero(mask)
    total_pixels = mask.size

    return germ_count, total_pixels


def parse_image_pairs(photo_dir):
    """
    Scans photo_dir for before/after image pairs.
    Handles various naming conventions:
    - run{N}_{wipe}_{before|after}
    - {wipe}_{before|after} (defaults to run 1 or parent run number)
    
    Returns:
        dict: Keyed by (run, wipe), value is a dict with 'before' and/or 'after' keys pointing to filename.
    """
    data_pairs = {}
    if not os.path.isdir(photo_dir):
        return data_pairs
        
    for filename in sorted(os.listdir(photo_dir)):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            # Ignore previously generated validation files
            if any(suffix in filename.lower() for suffix in ["_blue", "_mask", "_gray", "_validation"]):
                continue
                
            # Regex to find optional run, wipe name, and condition (before/after)
            # Support structures like run1_clorox_before, clorox_before, run1_lysol_before_cropped
            match = re.search(r"(?:run(\d+)_)?([a-zA-Z0-9_-]+)_(before|after)", filename.lower())
            if match:
                run_num_str, wipe_name, condition = match.groups()
                
                # Clean wipe name: remove trailing suffixes like '_cropped'
                wipe_name = re.sub(r'_(cropped|val|validation|mask|blue)$', '', wipe_name)
                
                # Determine run number: if not in filename, check parent directory name
                if run_num_str:
                    run_num = int(run_num_str)
                else:
                    # Look for digits in the directory name, e.g. "run1" -> 1
                    dir_match = re.search(r"run(\d+)", os.path.basename(os.path.abspath(photo_dir)).lower())
                    if dir_match:
                        run_num = int(dir_match.group(1))
                    else:
                        run_num = 1
                        
                key = (run_num, wipe_name)
                if key not in data_pairs:
                    data_pairs[key] = {}
                data_pairs[key][condition] = filename
                
    return data_pairs


def generate_chart(results, save_path):
    """
    Generates a bar chart comparing the Percent Removed for each wipe.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[Warning] matplotlib is not installed. Skipping chart generation.")
        return False
        
    if not results:
        print("[Warning] No results data to chart.")
        return False
        
    # Sort results by run and wipe name
    sorted_results = sorted(results, key=lambda x: (x['run'], x['wipe']))
    
    labels = [f"Run {r['run']} - {r['wipe']}" for r in sorted_results]
    values = [r['removed_pct'] for r in sorted_results]
    
    # Color scheme: Teal for cleaning, Red for spreading (negative values)
    colors = ['#2ec4b6' if v >= 0 else '#e71d36' for v in values]
    
    plt.figure(figsize=(10, 6))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Plot bars
    bars = plt.bar(labels, values, color=colors, edgecolor='black', alpha=0.85, width=0.6)
    
    # Add values on top (or bottom for negative) of bars
    for bar in bars:
        yval = bar.get_height()
        if yval >= 0:
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            plt.text(bar.get_x() + bar.get_width()/2.0, yval - 4.5, f"{yval:.1f}%", ha='center', va='top', fontsize=9, fontweight='bold', color='#d62728')
            
    plt.title("Germ Cleaning Efficiency by Wipe (Percent Removed)", fontsize=14, fontweight='bold', pad=15)
    plt.ylabel("Percent of Germs Removed (%)", fontsize=11, labelpad=10)
    plt.xlabel("Test Run & Wipe Brand", fontsize=11, labelpad=10)
    
    # Set y-limit with padding
    min_val = min(values) if values else 0
    max_val = max(values) if values else 100
    
    ymin = min(-10, min_val - 15) if min_val < 0 else 0
    ymax = max(100, max_val + 15)
    plt.ylim(ymin, ymax)
    
    # Add line at 0%
    plt.axhline(0, color='black', linewidth=0.8)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return True


def save_reports(results, output_dir):
    """
    Saves CSV and Markdown files containing analysis results.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Save CSV
    csv_path = os.path.join(output_dir, "results_summary.csv")
    try:
        with open(csv_path, "w") as f:
            f.write("Run,Wipe,Before_Germ_Count,Before_Total_Pixels,Before_Percent_Lit,After_Germ_Count,After_Total_Pixels,After_Percent_Lit,Percent_Removed\n")
            for r in results:
                f.write(f"{r['run']},{r['wipe']},{r['before_score']},{r['before_total']},{r['before_pct']:.4f}%,{r['after_score']},{r['after_total']},{r['after_pct']:.4f}%,{r['removed_pct']:.2f}%\n")
        print(f"[Info] Saved CSV summary to: {csv_path}")
    except Exception as e:
        print(f"[Error] Failed to write CSV file: {e}")
        
    # 2. Save Markdown
    md_path = os.path.join(output_dir, "results_summary.md")
    try:
        with open(md_path, "w") as f:
            f.write("# 🧪 Germ Cleaning Efficiency Report\n\n")
            f.write("This report was automatically generated by the Fluorescent Germ Analysis Tool.\n\n")
            f.write("## Summary Table\n\n")
            
            headers = ["Run", "Wipe Brand", "Before Germs", "Before Pixels", "Before Lit %", "After Germs", "After Pixels", "After Lit %", "Percent Removed"]
            row_format = "| " + " | ".join(["{}"] * len(headers)) + " |\n"
            separator = "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            f.write(row_format.format(*headers))
            f.write(separator)
            
            for r in results:
                removed_str = f"**{r['removed_pct']:.2f}%**" if r['removed_pct'] >= 0 else f"*{r['removed_pct']:.2f}% (Spread)*"
                f.write(row_format.format(
                    r['run'],
                    r['wipe'],
                    r['before_score'],
                    r['before_total'],
                    f"{r['before_pct']:.2f}%",
                    r['after_score'],
                    r['after_total'],
                    f"{r['after_pct']:.2f}%",
                    removed_str
                ))
                
            f.write("\n## 📊 Methodology & Formula\n")
            f.write("$$\\text{Percent Removed} = \\frac{\\text{Before\\% Lit} - \\text{After\\% Lit}}{\\text{Before\\% Lit}} \\times 100$$\n\n")
            f.write("A negative percent removed indicates that the 'germ' count increased or spread across the test surface after using the wipe.\n")
        print(f"[Info] Saved Markdown summary to: {md_path}")
    except Exception as e:
        print(f"[Error] Failed to write Markdown file: {e}")


def main():
    """
    Main execution entry point. Parses command line arguments if available,
    otherwise drops back to interactive inputs.
    """
    # Use argparse only if command line arguments are supplied
    # This keeps the user experience friendly for non-programmers using prompt-only
    use_args = len(sys.argv) > 1

    parser = argparse.ArgumentParser(description="Fluorescent Germ Analysis Tool for Science Alliance project.")
    parser.add_argument("-d", "--dir", type=str, help="Folder containing photo pairs to analyze.")
    parser.add_argument("-t", "--threshold", type=int, default=150, help="Brightness threshold (0-255). Default 150.")
    parser.add_argument("--no-crop", action="store_true", help="Disable center cropping.")
    parser.add_argument("--crop-ratios", type=float, nargs=4, default=[0.3, 0.7, 0.3, 0.7],
                        help="Custom crop percentages: y_start y_end x_start x_end. Range 0.0-1.0. Default: 0.3 0.7 0.3 0.7")
    parser.add_argument("--no-val", action="store_true", help="Do not save 'Proof' images.")
    parser.add_argument("--no-chart", action="store_true", help="Do not generate matplotlib bar chart comparison.")
    
    if use_args:
        args = parser.parse_args()
        photo_dir = args.dir
        threshold = args.threshold
        use_crop = not args.no_crop
        crop_ratios = args.crop_ratios
        save_val = not args.no_val
        generate_plots = not args.no_chart
    else:
        print("\n" + "="*50)
        print("      FLUORESCENT GERM ANALYSIS TOOL")
        print("      A Science Alliance Project by Zahra Anwar")
        print("="*50)
        
        photo_dir = input("\nEnter the folder path to analyze: ").strip()
        if not photo_dir:
            print("Error: Directory path is required.")
            return

        crop_choice = input("Crop to center to avoid edge noise? (y/n, default y): ").strip().lower()
        use_crop = crop_choice != 'n'
        crop_ratios = [0.3, 0.7, 0.3, 0.7]

        threshold_input = input("Enter brightness threshold (0-255, default 150): ").strip()
        try:
            threshold = int(threshold_input) if threshold_input else 150
        except ValueError:
            print("Invalid threshold. Using default 150.")
            threshold = 150

        save_choice = input("Save validation 'Proof' images? (y/n, default y): ").strip().lower()
        save_val = save_choice != 'n'
        generate_plots = True # Default true in interactive mode

    # Validate Photo Directory
    if not photo_dir or not os.path.isdir(photo_dir):
        print(f"Error: The directory '{photo_dir}' does not exist.")
        return

    # Parse and group images
    data_pairs = parse_image_pairs(photo_dir)

    if not data_pairs:
        print("\nNo matching image pairs found! Please ensure your files follow the format:")
        print("run1_wipe_before.png, run1_wipe_after.png, or clorox_before.jpg etc.")
        return

    # Setup Results Directories
    results_dir = os.path.join(photo_dir, "analysis_results")
    os.makedirs(results_dir, exist_ok=True)
    save_dir = results_dir if save_val else None

    print(f"\nAnalyzing image pairs with Blue Channel Extraction (Threshold: {threshold})...")
    if use_crop:
        print(f"Applying crop box bounds: Y({crop_ratios[0]:.2f}-{crop_ratios[1]:.2f}) X({crop_ratios[2]:.2f}-{crop_ratios[3]:.2f})")

    # Table format string
    header = f"{'Run':<4} | {'Wipe':<15} | {'Before Germs':<12} | {'Before Pixels':<13} | {'Before Lit %':<12} | {'After Germs':<11} | {'After Pixels':<12} | {'After Lit %':<11} | {'Percent Removed'}"
    separator = "-" * len(header)
    print("\n" + separator)
    print(header)
    print(separator)

    results_data = []

    # Process each pair
    for (run, wipe), conditions in sorted(data_pairs.items()):
        # Process 'Before'
        b_score = b_total = b_pct_val = 0
        b_pct_str = "N/A"
        has_before = 'before' in conditions
        if has_before:
            score, total = get_final_science_data(
                os.path.join(photo_dir, conditions['before']), 
                crop=use_crop, threshold=threshold, save_dir=save_dir, crop_ratios=crop_ratios
            )
            b_score, b_total = score, total
            b_pct_val = (score / total) if total > 0 else 0.0
            b_pct_str = f"{(b_pct_val * 100):.2f}%"

        # Process 'After'
        a_score = a_total = a_pct_val = 0
        a_pct_str = "N/A"
        has_after = 'after' in conditions
        if has_after:
            score, total = get_final_science_data(
                os.path.join(photo_dir, conditions['after']), 
                crop=use_crop, threshold=threshold, save_dir=save_dir, crop_ratios=crop_ratios
            )
            a_score, a_total = score, total
            a_pct_val = (score / total) if total > 0 else 0.0
            a_pct_str = f"{(a_pct_val * 100):.2f}%"

        # Calculate Percent Removed
        if has_before and has_after:
            if b_score > 0:
                removed_pct = ((b_pct_val - a_pct_val) / b_pct_val) * 100
                removed_str = f"{removed_pct:.2f}%"
            elif a_score > 0:
                # Started clean, but got dirty
                removed_pct = -100.0
                removed_str = "-100.00% (Added)"
            else:
                # No germs before or after
                removed_pct = 0.0
                removed_str = "0.00%"
        else:
            removed_pct = 0.0
            removed_str = "N/A"

        # Save details in list
        results_data.append({
            'run': run,
            'wipe': wipe,
            'before_score': b_score if has_before else "N/A",
            'before_total': b_total if has_before else "N/A",
            'before_pct': b_pct_val * 100 if has_before else 0.0,
            'after_score': a_score if has_after else "N/A",
            'after_total': a_total if has_after else "N/A",
            'after_pct': a_pct_val * 100 if has_after else 0.0,
            'removed_pct': removed_pct
        })

        # Print combined row
        b_score_str = str(b_score) if has_before else "N/A"
        b_total_str = str(b_total) if has_before else "N/A"
        a_score_str = str(a_score) if has_after else "N/A"
        a_total_str = str(a_total) if has_after else "N/A"
        
        print(f"{run:<4} | {wipe:<15} | {b_score_str:<12} | {b_total_str:<13} | {b_pct_str:<12} | {a_score_str:<11} | {a_total_str:<12} | {a_pct_str:<11} | {removed_str}")

    print(separator)

    # Save CSV and MD reports
    save_reports(results_data, results_dir)

    # Generate Chart comparison
    if generate_plots:
        chart_path = os.path.join(results_dir, "cleaning_efficiency_comparison.png")
        chart_success = generate_chart(results_data, chart_path)
        if chart_success:
            print(f"[Info] Saved comparison bar chart to: {chart_path}")

    print("\nAnalysis complete! Review the results in the directory:")
    print(f"  {results_dir}\n")


if __name__ == "__main__":
    main()
