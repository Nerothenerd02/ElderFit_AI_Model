import subprocess
import os

# Define paths to individual processing scripts
scripts = [
    "process_cat_cow.py",
    "process_sphinx.py",
    "process_tree.py",
    "process_deadlifts.py",
    "process_bird_dog.py",
    "process_chair_squats.py"
]

base_dir = r"D:\SCHOOL WORK\3RD YEAR\FYP\ELDERAI_Model\ELDERAI_Model\scripts"

# Loop through each script and execute it one by one
for script in scripts:
    script_path = os.path.join(base_dir, script)
    
    print(f"\n🚀 Running: {script} ...")
    
    try:
        subprocess.run(["python", script_path], check=True)
        print(f"✅ Completed: {script}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR running {script}: {e}")

# Final message
print("\n🎉✅ All exercises processed successfully!")
