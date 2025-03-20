import os

# Base directory for processed dataset
BASE_DIR = r"D:\SCHOOL WORK\3RD YEAR\FYP\ELDERAI_Model\ELDERAI_Model\data\data\processed"

# Define exercise categories
EXERCISES = {
    "yoga": ["cat-cow", "sphinx", "tree"],
    "gym": ["deadlifts", "bird_dog", "chair_squats"]
}

# Dictionary to store frame counts
frame_counts = {}

# Traverse each category and exercise
total_frames_dataset = 0

for category, exercises in EXERCISES.items():
    for exercise in exercises:
        exercise_path = os.path.join(BASE_DIR, category, exercise)

        if not os.path.exists(exercise_path):
            print(f"❌ ERROR: {exercise_path} not found!")
            continue

        frame_counts[exercise] = {"correct": 0, "incorrect": 0, "total": 0}

        # Process "correct" frames
        correct_path = os.path.join(exercise_path, "correct")
        if os.path.exists(correct_path):
            frame_counts[exercise]["correct"] = sum(
                len(files) for _, _, files in os.walk(correct_path) if any(f.endswith(".jpg") for f in files)
            )

        # Process "incorrect" frames (traverse subfolders)
        incorrect_path = os.path.join(exercise_path, "incorrect")
        if os.path.exists(incorrect_path):
            frame_counts[exercise]["incorrect"] = sum(
                len(files) for _, _, files in os.walk(incorrect_path) if any(f.endswith(".jpg") for f in files)
            )

        # Compute total for the exercise
        frame_counts[exercise]["total"] = frame_counts[exercise]["correct"] + frame_counts[exercise]["incorrect"]
        total_frames_dataset += frame_counts[exercise]["total"]

        # Print breakdown for each exercise
        print(f"\n📊 {exercise.upper()} Frames Count:")
        print(f"   ✅ Correct Form: {frame_counts[exercise]['correct']} frames")
        print(f"   ❌ Incorrect Form: {frame_counts[exercise]['incorrect']} frames")
        print(f"   🔢 Total Frames: {frame_counts[exercise]['total']} frames")

# Print total dataset frames
print("\n🎉 FINAL DATASET FRAME COUNT:")
print(f"📸 Total frames collected: {total_frames_dataset} frames\n")
