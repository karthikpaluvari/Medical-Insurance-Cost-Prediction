import shutil

print("🔓 Trying to unlock insurance.csv...")

src = "insurance.csv"
dst = "insurance_clean.csv"

try:
    shutil.copyfile(src, dst)
    print(f"✅ Unlocked copy created successfully: {dst}")
except PermissionError:
    print("❌ Still locked. Please ensure Excel or OneDrive is closed.")
except FileNotFoundError:
    print("❌ Could not find insurance.csv file. Place it in this folder and rerun.")
