import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
import os

# Load the MoveNet model from TensorFlow Hub
model_name = "movenet_thunder"  # Options: 'movenet_lightning', 'movenet_thunder'

try:
    if model_name == "movenet_lightning":
        module = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
    else:
        module = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
    print("✅ MoveNet Model Loaded Successfully!")
except Exception as e:
    print(f"❌ ERROR: Failed to load MoveNet model. \n{str(e)}")

# Define the mapping of keypoints to body parts
KEYPOINT_DICT = {
    'nose': 0, 'left_eye': 1, 'right_eye': 2, 'left_ear': 3, 'right_ear': 4,
    'left_shoulder': 5, 'right_shoulder': 6, 'left_elbow': 7, 'right_elbow': 8,
    'left_wrist': 9, 'right_wrist': 10, 'left_hip': 11, 'right_hip': 12,
    'left_knee': 13, 'right_knee': 14, 'left_ankle': 15, 'right_ankle': 16
}

# Define the connections between keypoints to draw lines for visualization
EDGES = [
    (0, 1), (0, 2), (1, 3), (2, 4), (0, 5), (0, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (5, 6), (5, 11), (6, 12), (11, 12), (11, 13), (13, 15), (12, 14), (14, 16)
]

def draw_keypoints(frame, keypoints, confidence_threshold=0.3):
    y, x, _ = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 4, (0, 255, 0), -1)

def draw_connections(frame, keypoints, edges, confidence_threshold=0.3):
    y, x, _ = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))
    for edge in edges:
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        if c1 > confidence_threshold and c2 > confidence_threshold:
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

def movenet(input_image):
    model = module.signatures['serving_default']
    input_image = tf.image.resize_with_pad(input_image, 256, 256)
    input_image = tf.cast(input_image, dtype=tf.int32)
    outputs = model(input_image)
    keypoints = outputs['output_0'].numpy()
    return keypoints

def process_video(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    os.makedirs(output_dir, exist_ok=True)
    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        input_image = tf.convert_to_tensor([frame], dtype=tf.uint8)
        keypoints = movenet(input_image)

        draw_connections(frame, keypoints, EDGES)
        draw_keypoints(frame, keypoints)

        output_path = os.path.join(output_dir, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(output_path, frame)
        frame_number += 1

    cap.release()

# ✅ Define base directory dynamically
BASE_DIR = r"D:\SCHOOL WORK\3RD YEAR\FYP\ElderAI_Model\ElderAI_Model"
DATA_DIR = os.path.join(BASE_DIR, "data", "data")
PROCESSED_ONE_DIR = os.path.join(DATA_DIR, "processed_one")
PROCESSED_TWO_DIR = os.path.join(DATA_DIR, "processed_two")

# ✅ Define subdirectories dynamically
CATEGORIES = ["yoga", "gym"]
EXERCISE = "tree"
FORM = "correct"
VIDEO_ID = "70"

# ✅ Define paths dynamically
video_path = os.path.join(PROCESSED_ONE_DIR, "yoga", EXERCISE, FORM, VIDEO_ID, "frame_0010.jpg")
output_dir = os.path.join(PROCESSED_TWO_DIR, "yoga", EXERCISE, FORM, VIDEO_ID)

# ✅ Print paths to verify
print(f"🎥 Video Path: {video_path}")
print(f"📂 Output Directory: {output_dir}")

# ✅ Run annotation test
process_video(video_path, output_dir)
