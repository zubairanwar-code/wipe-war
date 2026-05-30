#!/usr/bin/env python3
"""
Interactive Threshold & Crop Tuning Tool for Wipe-War Analysis

This tool allows you to visually adjust the crop area and brightness threshold 
on your test images in real-time, helping you find the perfect scientific settings.

Usage:
    uv run tune_threshold.py --image path/to/image.jpg
    or run interactively to choose a file.
"""

import cv2
import numpy as np
import os
import argparse
import sys

def main():
    # 1. Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="Tune threshold and crop settings for germ analysis.")
    parser.add_argument("-i", "--image", type=str, help="Path to the image to tune.")
    args = parser.parse_args()

    image_path = args.image

    # 2. Interactive prompt if no image is specified
    if not image_path:
        print("\n=== Fluorescent Germ Analyzer - Tuning Tool ===")
        image_path = input("Enter path to a test image file: ").strip()

    if not image_path or not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        sys.exit(1)

    # 3. Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image at '{image_path}' with OpenCV.")
        sys.exit(1)

    print(f"\nLoaded image: {image_path} ({img.shape[1]}x{img.shape[0]})")
    print("Opening interactive window. Use the sliders to adjust settings.")
    print("Press 'q' or 'ESC' to quit and print the selected settings.")

    # 4. Create Window
    window_name = "Germ Analyzer Tuner - Press 'q' to Quit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1200, 750)

    # Trackbar Callback (do nothing, we read values in the loop)
    def nothing(x):
        pass

    # Create Trackbars
    # Defaults correspond to code.py defaults (Threshold=150, Crop 30% to 70%)
    cv2.createTrackbar("Threshold", window_name, 150, 255, nothing)
    cv2.createTrackbar("Crop Y Start %", window_name, 30, 100, nothing)
    cv2.createTrackbar("Crop Y End %", window_name, 70, 100, nothing)
    cv2.createTrackbar("Crop X Start %", window_name, 30, 100, nothing)
    cv2.createTrackbar("Crop X End %", window_name, 70, 100, nothing)

    h, w, _ = img.shape

    while True:
        # Get current trackbar positions
        threshold = cv2.getTrackbarPos("Threshold", window_name)
        y_start_pct = cv2.getTrackbarPos("Crop Y Start %", window_name)
        y_end_pct = cv2.getTrackbarPos("Crop Y End %", window_name)
        x_start_pct = cv2.getTrackbarPos("Crop X Start %", window_name)
        x_end_pct = cv2.getTrackbarPos("Crop X End %", window_name)

        # Enforce minimum sizes and order (start must be < end)
        if y_start_pct >= y_end_pct:
            y_start_pct = max(0, y_end_pct - 1)
        if x_start_pct >= x_end_pct:
            x_start_pct = max(0, x_end_pct - 1)

        # Calculate pixel coordinates
        y1, y2 = int(h * (y_start_pct / 100.0)), int(h * (y_end_pct / 100.0))
        x1, x2 = int(w * (x_start_pct / 100.0)), int(w * (x_end_pct / 100.0))

        # 1. Original Image with Crop Rectangle Overlay
        orig_disp = img.copy()
        cv2.rectangle(orig_disp, (x1, y1), (x2, y2), (0, 255, 0), 4) # Green box
        
        # 2. Extract ROI and Blue Channel
        roi = img[y1:y2, x1:x2]
        if roi.size == 0:
            continue
            
        blue_channel = roi[:, :, 0] # Blue channel extraction

        # 3. Apply Threshold to get mask
        _, mask = cv2.threshold(blue_channel, threshold, 255, cv2.THRESH_BINARY)

        # Convert single-channel views back to BGR for display concatenation
        blue_bgr = cv2.cvtColor(blue_channel, cv2.COLOR_GRAY2BGR)
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # Add text overlays to views
        cv2.putText(orig_disp, "Original (Crop Box in Green)", (30, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.putText(blue_bgr, f"Blue Channel (ROI)", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 120, 0), 2)
        
        # Calculate lit percentage to display on mask
        germ_count = np.count_nonzero(mask)
        total_pixels = mask.size
        lit_pct = (germ_count / total_pixels * 100) if total_pixels > 0 else 0
        cv2.putText(mask_bgr, f"Binary Mask: {germ_count} / {total_pixels} ({lit_pct:.2f}%)", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Resize ROI views to fit side-by-side nicely
        roi_h = y2 - y1
        roi_w = x2 - x1
        
        # We resize the blue & mask views to match the height of the original display for layout
        target_h = orig_disp.shape[0]
        # Maintain aspect ratio for the ROI display
        target_w = int(roi_w * (target_h / 2.0 / roi_h)) if roi_h > 0 else 100
        
        blue_resized = cv2.resize(blue_bgr, (target_w, target_h // 2))
        mask_resized = cv2.resize(mask_bgr, (target_w, target_h // 2))
        
        # Stack ROI views vertically
        roi_stacked = np.vstack((blue_resized, mask_resized))

        # Concatenate original view and ROI views horizontally
        canvas = np.hstack((orig_disp, roi_stacked))

        # Show the display canvas
        cv2.imshow(window_name, canvas)

        # Break loop on 'q' or ESC key
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == 27:
            break

    cv2.destroyAllWindows()

    # Print final settings for copy-pasting
    print("\n" + "="*50)
    print("             TUNED PARAMETERS")
    print("="*50)
    print(f"Threshold: {threshold}")
    print(f"Crop Box: Y: {y_start_pct}% - {y_end_pct}%, X: {x_start_pct}% - {x_end_pct}%")
    print(f"Python Args for code.py:")
    print(f"  --threshold {threshold} " + 
          (f"--crop-ratios {y_start_pct / 100.0} {y_end_pct / 100.0} {x_start_pct / 100.0} {x_end_pct / 100.0}" if (y_start_pct != 30 or y_end_pct != 70 or x_start_pct != 30 or x_end_pct != 70) else ""))
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
