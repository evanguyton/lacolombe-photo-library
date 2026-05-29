#!/usr/bin/env python3
"""
La Colombe Photo Library — auto-sort script
Moves files in the repo root into themed folders based on filename keywords.
Run from inside the lacolombe-photo-library repo folder.

Usage:
  cd ~/path/to/lacolombe-photo-library
  python3 sort_photos.py
  git push
"""

import os, shutil

# ── Folder → keyword patterns (lowercase match against filename) ──────────────
RULES = [
    ("origin",   ["ardi", "burundi", "brazil", "haiti", "kerinci", "ethiopia",
                  "colombia", "peru", "guatemala", "rwanda", "sumatra", "kenya",
                  "yirgacheffe", "bourbon", "bastilla", "barranca", "cherry",
                  "cherries", "drying", "farm", "mill", "harvest", "plant",
                  "flower", "bean", "green_bean", "roastery", "origin",
                  "village", "volcano", "landscape", "hillside", "warehouse"]),

    ("cafes",    ["cafe", "coffee_shop", "workshop", "interior", "noho", "dc",
                  "fishtown", "uline", "chicago", "nyc", "boston", "bar",
                  "counter", "espresso_bar"]),

    ("barista",  ["barista", "pour", "pull", "shot", "latte_art", "tamping",
                  "portafilter", "steam", "staff", "crew"]),

    ("product",  ["draft_latte", "can", "mug", "cup", "cortado", "latte",
                  "espresso", "matcha", "cold_brew", "drinkware", "deruta",
                  "packaging", "bag", "box", "triple", "seasonal"]),

    ("campaign", ["ooh", "campaign", "mrsmr", "poster", "billboard",
                  "street", "delivery", "van", "fleet"]),

    ("people",   ["portrait", "smile", "community", "team", "family",
                  "women", "farmer", "grower", "partner"]),
]

EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

def folder_for(filename):
    name = filename.lower().replace("-", "_").replace(" ", "_")
    for folder, keywords in RULES:
        if any(kw in name for kw in keywords):
            return folder
    return "unsorted"   # catch-all for anything that doesn't match

def main():
    repo = os.path.dirname(os.path.abspath(__file__))
    moved = {}

    for fname in os.listdir(repo):
        if os.path.splitext(fname)[1] not in EXTENSIONS:
            continue
        if os.path.isdir(os.path.join(repo, fname)):
            continue

        dest_folder = folder_for(fname)
        dest_dir = os.path.join(repo, dest_folder)
        os.makedirs(dest_dir, exist_ok=True)

        src = os.path.join(repo, fname)
        dst = os.path.join(dest_dir, fname)

        # avoid overwriting
        if os.path.exists(dst):
            base, ext = os.path.splitext(fname)
            dst = os.path.join(dest_dir, f"{base}_dup{ext}")

        shutil.move(src, dst)
        moved.setdefault(dest_folder, []).append(fname)

    # summary
    print("\n✅ Sorted photos:\n")
    for folder, files in sorted(moved.items()):
        print(f"  {folder}/  ({len(files)} files)")
        for f in files:
            print(f"    {f}")

    print(f"\nTotal moved: {sum(len(v) for v in moved.values())}")
    print("\nNow run:\n  git add -A && git commit -m 'Auto-sort photos into folders' && git push")

if __name__ == "__main__":
    main()
