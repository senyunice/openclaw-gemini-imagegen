import cv2
import numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama

def lama_inpaint(image_path, output_path, margin=80):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: cannot read {image_path}")
        return

    h, w = img.shape[:2]
    print(f"Image: {w}x{h}")

    # Watermark region (bottom-right)
    if w > 1024 and h > 1024:
        logo_size, margin_right, margin_bottom = 96, 64, 96
    else:
        logo_size, margin_right, margin_bottom = 48, 32, 48

    x1 = w - margin_right - logo_size
    y1 = h - margin_bottom - logo_size
    x2, y2 = x1 + logo_size, y1 + logo_size

    print(f"Watermark: ({x1},{y1}) to ({x2},{y2})")

    # Create mask (slightly larger area)
    mask = np.zeros((h, w), dtype=np.uint8)
    # Expand the mask region
    ex = 40  # extra pixels around watermark
    mx1 = max(0, x1 - ex)
    my1 = max(0, y1 - ex)
    mx2 = min(w, x2 + ex)
    my2 = min(h, y2 + ex)
    mask[my1:my2, mx1:mx2] = 255

    # Dilate mask slightly
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Convert to PIL
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    mask_pil = Image.fromarray(mask)

    print("Loading Lama model...")
    model = SimpleLama()

    print("Inpainting...")
    result = model(img_pil, mask_pil)

    # Convert back to OpenCV
    result_cv = cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, result_cv)
    import os
    print(f"Done: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: lama_inpaint.py <input> <output>")
        sys.exit(1)
    lama_inpaint(sys.argv[1], sys.argv[2])
