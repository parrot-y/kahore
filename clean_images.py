#!/usr/bin/env python3
import shutil
import os

IMG = "/home/kali/Documents/garage-ruaka/assets/img"
HERO = f"{IMG}/hero"

# Original high-quality photos from user
SHOP_FRONT = f"{HERO}/photo_2026-02-24_06-12-49.jpg"     # The Caltex/Shop image
SHOP_INTERIOR = f"{HERO}/photo_2026-02-17_19-22-15.jpg"  # Interior with woman (I'll use original)
FOX3D_UNIT = f"{HERO}/photo_2026-02-24_05-13-36.jpg"     # Alignment screen

def safe_copy(src, dst):
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"  ✅ Copied {os.path.basename(src)} to {os.path.basename(dst)}")

# 1. Update the 'clean' hero images to be EXACT COPIES of originals (avoiding any resizing/stretching)
# Slide 1: Interior
safe_copy(SHOP_INTERIOR, f"{HERO}/hero_kahore_1_clean.jpg")
# Slide 2: Shop Front
safe_copy(SHOP_FRONT, f"{HERO}/hero_kahore_2_clean.jpg")
# Slide 3: Screen
safe_copy(FOX3D_UNIT, f"{HERO}/hero_kahore_3_clean.jpg")

# 2. Update stock targets with the direct originals
# Why Choose Us features
safe_copy(SHOP_FRONT, f"{IMG}/feature_img_1.jpg")
safe_copy(SHOP_INTERIOR, f"{IMG}/feature_img_2.jpg")
safe_copy(FOX3D_UNIT, f"{IMG}/feature_img_3.jpg")

# Portfolio and Before/After
safe_copy(SHOP_FRONT, f"{IMG}/portfolio_img_1.jpg")   # Truck Upgrade
safe_copy(FOX3D_UNIT, f"{IMG}/portfolio_img_2.jpg")   # FOX3D Alignment
safe_copy(SHOP_INTERIOR, f"{IMG}/portfolio_img_3.jpg") # Rim Customisation
safe_copy(SHOP_FRONT, f"{IMG}/portfolio_img_4.jpg")   # Battery

# Before/After targets
safe_copy(SHOP_INTERIOR, f"{IMG}/before_img_1.jpg")
safe_copy(SHOP_FRONT, f"{IMG}/after_img_1.jpg")

# Service images
safe_copy(FOX3D_UNIT, f"{IMG}/service_img_1.jpg")
safe_copy(SHOP_FRONT, f"{IMG}/service_img_2.jpg")
safe_copy(SHOP_INTERIOR, f"{IMG}/service_img_3.jpg")

print("\nFiles restored from originals (No stretching). Now update CSS to ensure proper display.")
