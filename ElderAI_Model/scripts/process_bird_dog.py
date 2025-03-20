import os
from extract_frames import capture_frames

def process_exercise(exercise_name):
    """
    Process all videos for a specific exercise and extract frames.

    :param exercise_name: Name of the exercise (e.g., "cat-cow")
    """
    base_dir = r"D:\SCHOOL WORK\3RD YEAR\FYP\ELDERAI_Model\ELDERAI_Model"
    raw_dir = os.path.join(base_dir, "data", "data", "raw", "gym", exercise_name)
    processed_dir = os.path.join(base_dir, "data", "data", "processed", "gym", exercise_name)

    if not os.path.exists(raw_dir):
        print(f"❌ ERROR: Folder not found: {raw_dir}")
        return

    total_videos = 0
    videos_processed = 0
    total_frames = 0

    # Traverse both "correct" and "incorrect" folders
    for correctness_label in ["correct", "incorrect"]:
        label_path = os.path.join(raw_dir, correctness_label)
        processed_label_path = os.path.join(processed_dir, correctness_label)

        if not os.path.exists(label_path):
            print(f"⚠️ Skipping {label_path} (Not Found)")
            continue

        # If processing "correct" folder, process videos directly
        if correctness_label == "correct":
            videos = [f for f in os.listdir(label_path) if f.endswith(".mp4")]
            total_videos += len(videos)

            for video_file in videos:
                video_path = os.path.join(label_path, video_file)
                video_name = os.path.splitext(video_file)[0]

                # Store frames in a folder per video
                output_subdir = os.path.join(processed_label_path, video_name)
                os.makedirs(output_subdir, exist_ok=True)

                print(f"🔄 Processing: {video_file} → {output_subdir}")
                frames_extracted = capture_frames(video_path, output_subdir)

                if frames_extracted > 0:
                    videos_processed += 1
                    total_frames += frames_extracted

        # If processing "incorrect" folder, traverse subfolders
        elif correctness_label == "incorrect":
            for error_category in os.listdir(label_path):  # e.g., "arm_not_shoulder_length", "head_movement"
                error_path = os.path.join(label_path, error_category)
                processed_error_path = os.path.join(processed_label_path, error_category)

                if not os.path.isdir(error_path):
                    continue

                videos = [f for f in os.listdir(error_path) if f.endswith(".mp4")]
                total_videos += len(videos)

                for video_file in videos:
                    video_path = os.path.join(error_path, video_file)
                    video_name = os.path.splitext(video_file)[0]

                    # Store frames in a folder per error category → per video
                    output_subdir = os.path.join(processed_error_path, video_name)
                    os.makedirs(output_subdir, exist_ok=True)

                    print(f"🔄 Processing: {video_file} in {error_category} → {output_subdir}")
                    frames_extracted = capture_frames(video_path, output_subdir)

                    if frames_extracted > 0:
                        videos_processed += 1
                        total_frames += frames_extracted

    print(f"\n✅ Completed processing for {exercise_name}.")
    print(f"📝 Processed {videos_processed}/{total_videos} videos")
    print(f"📸 Total frames extracted: {total_frames}\n")

# Run for bird-dog
process_exercise("bird_dog")
