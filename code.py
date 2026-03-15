import cv2
import numpy as np
import os

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
    print("="*50)

    # 1. Folder Selection
    photo_dir = input("\nEnter the folder path to analyze: ").strip()
    
    if not os.path.isdir(photo_dir):
        print(f"Error: The directory '{photo_dir}' does not exist.")
        return

    # 2. Configuration Settings
    crop_choice = input("Crop to center to avoid edge noise? (y/n): ").strip().lower()
    use_crop = crop_choice == 'y'

    use_pct = input("Show results as a percentage of the total area? (y/n): ").strip().lower() == 'y'

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

    print(f"\nAnalyzing images with Blue Channel Extraction (Threshold: {threshold})...")
    print("-" * 65)
    print(f"{'Filename':<30} | {'Germ Score':<10} | {'% Coverage' if use_pct else 'Total Area'}")
    print("-" * 65)

    # 4. Process Files
    found_images = False
    for filename in sorted(os.listdir(photo_dir)):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(photo_dir, filename)
            
            germ_score, total_px = get_final_science_data(
                image_path, crop=use_crop, threshold=threshold, save_dir=save_dir
            )
            
            if use_pct and total_px > 0:
                percent_lit = (germ_score / total_px) * 100
                print(f"{filename:<30} | {germ_score:<10} | {percent_lit:.4f}%")
            else:
                print(f"{filename:<30} | {germ_score:<10} | {total_px}")
            
            found_images = True

    if not found_images:
        print("No images found! Please check the folder path.")
    else:
        print("-" * 65)
        print("\nAnalysis complete!")
        print("Use these scores to calculate 'Percent Removed' using this formula:")
        print("((Before_Score - After_Score) / Before_Score) * 100")


if __name__ == "__main__":
    main()
