"""
Configuration file for YOLO Object Detection
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if they don't exist
for dir_path in [MODELS_DIR, INPUT_DIR, OUTPUT_DIR, TEMP_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Model configurations
MODEL_CONFIGS = {
    "yolov8n": {
        "name": "YOLOv8-Nano",
        "size": "640",
        "speed": "fast",
        "accuracy": "medium",
        "url": "yolov8n.pt"
    },
    "yolov8s": {
        "name": "YOLOv8-Small",
        "size": "640",
        "speed": "fast",
        "accuracy": "good",
        "url": "yolov8s.pt"
    },
    "yolov8m": {
        "name": "YOLOv8-Medium",
        "size": "640",
        "speed": "medium",
        "accuracy": "high",
        "url": "yolov8m.pt"
    },
    "yolov8l": {
        "name": "YOLOv8-Large",
        "size": "640",
        "speed": "slow",
        "accuracy": "very high",
        "url": "yolov8l.pt"
    },
    "yolov8x": {
        "name": "YOLOv8-Extra Large",
        "size": "640",
        "speed": "very slow",
        "accuracy": "highest",
        "url": "yolov8x.pt"
    }
}

# Default model
DEFAULT_MODEL = "yolov8m"

# Detection parameters
DETECTION_PARAMS = {
    "conf_threshold": 0.25,
    "iou_threshold": 0.45,
    "max_det": 300,
    "classes": None,  # None for all classes
    "agnostic_nms": False,
    "augment": False,
    "half": False,
    "vid_stride": 1
}

# COCO class names (80 classes)
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
    "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop",
    "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush"
]

# Output settings
OUTPUT_SETTINGS = {
    "save_images": True,
    "save_videos": True,
    "save_json": True,
    "save_csv": True,
    "show_confidence": True,
    "show_labels": True,
    "line_thickness": 2,
    "font_size": 0.5,
    "color_scheme": "default"  # default, random, custom
}

# Custom colors for classes (BGR format)
CUSTOM_COLORS = {
    "person": (0, 255, 0),
    "car": (255, 0, 0),
    "truck": (0, 0, 255),
    "bicycle": (255, 255, 0),
    "motorcycle": (255, 0, 255),
    "bus": (0, 255, 255)
}

# Video processing settings
VIDEO_SETTINGS = {
    "fps": 30,
    "buffer_size": 1,
    "fourcc": "mp4v",
    "resize": None,  # (width, height) or None
    "skip_frames": 0,
    "process_every_n_frames": 1
}

# Tracking settings
TRACKING_SETTINGS = {
    "enabled": False,
    "tracker_type": "bytetrack",  # bytetrack, botsort
    "track_buffer": 30
}

# Hardware settings
HARDWARE_SETTINGS = {
    "device": "auto",  # auto, cpu, cuda, mps
    "workers": 8,
    "batch_size": 16,
    "half_precision": False
}

# Logging settings
LOGGING_SETTINGS = {
    "level": "INFO",
    "log_file": OUTPUT_DIR / "detection.log",
    "console_output": True
}
