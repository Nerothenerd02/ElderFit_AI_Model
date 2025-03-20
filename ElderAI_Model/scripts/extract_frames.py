import cv2
import os
import numpy as np  # Import numpy for normalization

def capture_frames(video_path, output_dir, target_size=(256, 256)):
    """
    Extracts all frames from a video, resizes them, normalizes them (0-1), and saves them.

    :param video_path: Path to the input video
    :param output_dir: Directory to save extracted frames
    :param target_size: Resize dimensions (height, width)
    """

    # Resolve absolute paths
    video_path = os.path.abspath(video_path)
    output_dir = os.path.abspath(output_dir)

    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"❌ ERROR: Video file not found at {video_path}")
        return 0
    
    print(f"✅ Processing video: {video_path}")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ ERROR: Unable to open {video_path}")
        return 0
    
    print("🎥 Video successfully opened!")

    frame_count = 0
    saved_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get total frame count
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Get FPS

    print(f"📽 FPS: {fps}, Total Frames: {total_frames}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Resize the frame
        frame_resized = cv2.resize(frame, target_size)

        # ✅ Normalize pixel values to 0-1 range
        frame_normalized = frame_resized.astype('float32') / 255.0

        # Convert back to 0-255 range for saving (avoid dark images)
        frame_to_save = (frame_normalized * 255).astype('uint8')

        # Save frame
        frame_filename = f"frame_{saved_count:04d}.jpg"
        frame_path = os.path.join(output_dir, frame_filename)
        cv2.imwrite(frame_path, frame_to_save)

        saved_count += 1
        frame_count += 1

    cap.release()
    print(f"✅ Extracted {saved_count} frames from {video_path} → {output_dir}\n")
    return saved_count

# Example usage:
video_path = r"D:\SCHOOL WORK\3RD YEAR\FYP\ELDERAI_Model\ELDERAI_Model\data\data\raw\yoga\cat-cow\correct\61.mp4"
output_dir = r"D:\SCHOOL WORK\3RD YEAR\FYP\ELDERAI_Model\ELDERAI_Model\data\data\processed\yoga\cat-cow\correct"

capture_frames(video_path, output_dir)
