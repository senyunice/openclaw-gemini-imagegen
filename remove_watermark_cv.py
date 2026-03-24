import cv2
import numpy as np
from PIL import Image

def remove_watermark_opencv(image_path, output_path):
    """Remove watermark using OpenCV inpainting (TELEA algorithm)"""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: cannot read {image_path}")
        return

    h, w = img.shape[:2]
    print(f"Image size: {w}x{h}")

    # Watermark position (bottom-right, Gemini style)
    if w > 1024 and h > 1024:
        logo_size, margin_right, margin_bottom = 96, 64, 64
    else:
        logo_size, margin_right, margin_bottom = 48, 32, 32

    x1 = w - margin_right - logo_size
    y1 = h - margin_bottom - logo_size
    x2, y2 = x1 + logo_size, y1 + logo_size

    print(f"Watermark region: ({x1},{y1}) to ({x2},{y2})")

    # Create mask for watermark area
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255

    # Dilate mask slightly for better blending
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Apply inpainting (TELEA algorithm - works well for watermark removal)
    result = cv2.inpaint(img, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

    cv2.imwrite(output_path, result)
    import os
    print(f"Saved: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: remove_watermark_cv.py <input> <output>")
        sys.exit(1)
    remove_watermark_opencv(sys.argv[1], sys.argv[2])
