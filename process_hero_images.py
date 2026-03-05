#!/usr/bin/env python3
"""
Hero Image Processor for Junction Kahore Tyres Ltd website.

HOW TO USE:
  1. Save your 3 hero images into:
       assets/img/hero/hero_kahore_1.jpg   (FOX3D machine + KAHORE TYRES sign)
       assets/img/hero/hero_kahore_2.jpg   (Street view with Junction Kahore Tyres Ltd sign)
       assets/img/hero/hero_kahore_3.jpg   (Inside shop - has woman sitting on left)
  2. Run:  python3 process_hero_images.py
  3. Processed images will be saved as:
       assets/img/hero/hero_1_clean.jpg
       assets/img/hero/hero_2_clean.jpg
       assets/img/hero/hero_3_clean.jpg
"""

from PIL import Image, ImageEnhance, ImageFilter
import os

HERO_DIR = "assets/img/hero"
INPUTS = [
    ("hero_kahore_1.jpg", "hero_1_clean.jpg", None),           # Full image, just enhance
    ("hero_kahore_2.jpg", "hero_2_clean.jpg", None),           # Full image, just enhance
    ("hero_kahore_3.jpg", "hero_3_clean.jpg", "crop_left"),    # Remove woman (crop left 22%)
]

def enhance(img):
    """Apply aesthetic improvements: brightness, contrast, colour, sharpness."""
    img = ImageEnhance.Brightness(img).enhance(1.18)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    img = ImageEnhance.Color(img).enhance(1.30)       # Richer, more vibrant colours
    img = ImageEnhance.Sharpness(img).enhance(1.40)   # Crisper details
    return img

def remove_woman_left(img):
    """
    The woman sits on the far left side (~left 22% of the image).
    We crop from 22% to the right edge, keeping the alignment machine
    + storage cage + Michelin sign fully visible.
    """
    w, h = img.size
    crop_from_x = int(w * 0.22)
    cropped = img.crop((crop_from_x, 0, w, h))
    # Scale back to original width so it fills the hero banner properly
    result = cropped.resize((w, h), Image.LANCZOS)
    return result

processed = []
errors = []

for input_name, output_name, transform in INPUTS:
    src = os.path.join(HERO_DIR, input_name)
    dst = os.path.join(HERO_DIR, output_name)

    if not os.path.exists(src):
        errors.append(f"  MISSING: {src}")
        continue

    try:
        img = Image.open(src).convert("RGB")

        if transform == "crop_left":
            img = remove_woman_left(img)

        img = enhance(img)
        img.save(dst, "JPEG", quality=92, optimize=True)
        processed.append(f"  ✅ {input_name}  →  {output_name}")
    except Exception as e:
        errors.append(f"  ERROR {input_name}: {e}")

print("\n=== Junction Kahore Hero Image Processor ===\n")
if processed:
    print("Processed:")
    print("\n".join(processed))
if errors:
    print("\nProblems:")
    print("\n".join(errors))
    print("\n⚠️  Make sure all 3 images are in:", HERO_DIR)
else:
    print("\n✅ All done! Refresh http://localhost:8080 to see the new hero images.")
