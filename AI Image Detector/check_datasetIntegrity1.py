# check_dataset_integrity.py
import os
from PIL import Image, ImageFile
from tqdm import tqdm

# Allow PIL to attempt to load truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Directories to check
data_dirs = ["data_binary", "data_multiclass"]

# Allowed extensions
allowed_exts = [".jpg", ".jpeg", ".png"]

corrupted_files = []
bad_extension_files = []
zero_byte_files = []

for base_dir in data_dirs:
    for root, dirs, files in os.walk(base_dir):
        # tqdm progress bar for each folder
        for file in tqdm(files, desc=f"Checking {base_dir}", unit="file"):
            filepath = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            # Check extension
            if ext not in allowed_exts:
                bad_extension_files.append(filepath)
                continue

            # Check for zero-byte files
            if os.path.getsize(filepath) == 0:
                zero_byte_files.append(filepath)
                continue

            # Check if image can be opened
            try:
                img = Image.open(filepath)
                img.verify()  # Verify image integrity
            except Exception:
                corrupted_files.append(filepath)

# Print results
print("\n=== Zero-byte files ===")
for f in zero_byte_files:
    print(f)

print("\n=== Corrupted images ===")
for f in corrupted_files:
    print(f)

print("\n=== Files with unacceptable extensions ===")
for f in bad_extension_files:
    print(f)

# Optional: save to a text file
with open("problematic_files.txt", "w") as f:
    if zero_byte_files:
        f.write("=== Zero-byte files ===\n")
        for item in zero_byte_files:
            f.write(item + "\n")
    if corrupted_files:
        f.write("\n=== Corrupted images ===\n")
        for item in corrupted_files:
            f.write(item + "\n")
    if bad_extension_files:
        f.write("\n=== Files with unacceptable extensions ===\n")
        for item in bad_extension_files:
            f.write(item + "\n")
