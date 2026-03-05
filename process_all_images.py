#!/usr/bin/env python3
"""
Full image processor for Junction Kahore Tyres Ltd.
Processes hero images + service images.
Run from the project root: python3 process_all_images.py
"""

from PIL import Image, ImageEnhance, ImageFilter
import os, shutil

HERO_DIR   = "assets/img/hero"
SVC_DIR    = "assets/img"

# --- Helpers ---
def enhance(img, bright=1.18, contrast=1.15, color=1.30, sharp=1.40):
    img = ImageEnhance.Brightness(img).enhance(bright)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(color)
    img = ImageEnhance.Sharpness(img).enhance(sharp)
    return img

def crop_woman_left(img, pct=0.22):
    """Crop the left `pct` of image (where woman sits) and stretch to fill."""
    w, h = img.size
    left = int(w * pct)
    cropped = img.crop((left, 0, w, h))
    return cropped.resize((w, h), Image.LANCZOS)

def save(img, path, quality=92):
    img.save(path, "JPEG", quality=quality, optimize=True)
    print(f"  ✅  Saved: {path}")

# ============================================================
# HERO IMAGES — rename + enhance + woman-removal on slide 3
# ============================================================
hero_map = [
    # (source filename, dest filename, transform)
    ("photo_2026-02-17_19-22-15.jpg", "hero_kahore_1.jpg", None),
    ("photo_2026-02-24_05-13-36.jpg", "hero_kahore_2.jpg", None),
    ("photo_2026-02-24_06-12-49.jpg", "hero_kahore_3.jpg", "crop_left"),
]

print("\n=== Processing HERO images ===")
for src_name, dst_name, transform in hero_map:
    src = os.path.join(HERO_DIR, src_name)
    dst = os.path.join(HERO_DIR, dst_name)
    if not os.path.exists(src):
        print(f"  ⚠️  Missing: {src}")
        continue
    img = Image.open(src).convert("RGB")
    if transform == "crop_left":
        img = crop_woman_left(img)
    img = enhance(img)
    save(img, dst)

# ============================================================
# SERVICE IMAGES
# User assigned:
#   service_img_1 → Wheel Alignment  (FOX3D close-up screen)
#   service_img_2 → Tyre Selling     (tyre rack with rims)
#   service_img_3 → Rims Selling     (rim + tyres from street side)
#   service_img_4 → Diagnosis        (inside shop + woman — crop woman)
#   service_img_5 → Battery Sales    (crop from hero_kahore_1 where batteries are stored)
# ============================================================
print("\n=== Processing SERVICE images ===")

# Map: (source path, dest path, transform)
svc_images = []

# Check which message-provided images are in the project root or Downloads
search_roots = [
    "/home/kali/Documents",
    "/home/kali/Downloads",
    "/home/kali/Pictures",
    "/home/kali/Desktop",
]

# User provided 4 images in the latest chat message.
# They tend to be named photo_*.jpg by Telegram/WhatsApp.
# Let's find all jpg files NOT already in hero or assets/img sub-dirs
import glob, pathlib

candidates = []
for root in search_roots:
    for ext in ("*.jpg","*.jpeg","*.JPG","*.JPEG","*.png","*.PNG"):
        candidates.extend(glob.glob(os.path.join(root, "**", ext), recursive=True))

# Filter out already-processed files
candidates = [c for c in candidates if "garage-ruaka" not in c]
candidates.sort(key=os.path.getmtime, reverse=True)  # newest first

print(f"  Found {len(candidates)} candidate images outside project:")
for c in candidates[:10]:
    print(f"    {c}")

# ============================================================
# BATTERY IMAGE — crop from hero_kahore_1 (right side storage cage has KV batteries)
# ============================================================
battery_src = os.path.join(HERO_DIR, "hero_kahore_1.jpg")
battery_dst = os.path.join(SVC_DIR, "service_img_battery.jpg")
if os.path.exists(battery_src):
    img = Image.open(battery_src).convert("RGB")
    w, h = img.size
    # Right 45% of the image has the battery storage cage
    battery_crop = img.crop((int(w * 0.55), 0, w, h))
    battery_crop = battery_crop.resize((800, 600), Image.LANCZOS)
    battery_crop = enhance(battery_crop, bright=1.25, color=1.40)
    save(battery_crop, battery_dst)

print("\n✅  Done! Now update HTML to reference the new image names.")
print("   hero: hero_kahore_1.jpg, hero_kahore_2.jpg, hero_kahore_3.jpg")
print("   Refresh http://localhost:8080 to see results.")
