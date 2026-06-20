# YOLO Object Detection - Advanced Implementation

An advanced, production-ready YOLO (You Only Look Once) object detection project using Ultralytics YOLOv8. This project supports image, video, webcam, and batch processing with comprehensive export capabilities and performance optimization.

## Features

- **Multiple Input Types**: Images, videos, webcam streams, and batch processing
- **Multiple Model Sizes**: YOLOv8 Nano, Small, Medium, Large, and Extra Large
- **Advanced Detection**: Customizable confidence and IOU thresholds
- **Export Options**: JSON, CSV formats for detection results
- **Performance Optimization**: GPU acceleration, batch processing, benchmarking
- **Visualization**: Customizable bounding boxes, labels, and confidence scores
- **Utility Functions**: Image processing, filtering, statistics, and visualization
- **Logging**: Comprehensive logging for debugging and monitoring

## Project Structure

```
yolo object detection/
├── detector.py           # Main detection module
├── config.py             # Configuration settings
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── models/              # Downloaded YOLO models (auto-created)
├── input/               # Input images/videos (auto-created)
├── output/              # Detection results (auto-created)
└── temp/                # Temporary files (auto-created)
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster inference

### Installation

1. **Navigate to the project directory**:
```bash
cd "d:\swayam pandit\purvanchal\SEM3\PYTHON\coding practice\opencv_master_project\project\yolo object detection"
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
```

3. **Activate the virtual environment**:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Verify installation**:
```bash
python -c "import ultralytics; import cv2; import torch; print('All dependencies installed successfully!')"
```

## Usage Guide

### Basic Usage

#### 1. Image Detection

Detect objects in a single image:

```bash
python detector.py --input path/to/image.jpg
```

**With custom parameters:**
```bash
python detector.py --input path/to/image.jpg --model yolov8m --conf 0.5 --iou 0.4 --show
```

#### 2. Video Detection

Detect objects in a video:

```bash
python detector.py --input path/to/video.mp4
```

#### 3. Webcam Detection

Detect objects from webcam:

```bash
python detector.py --webcam
```

**With specific camera:**
```bash
python detector.py --webcam --camera-id 1
```

#### 4. Batch Processing

Process all images in a directory:

```bash
python detector.py --input path/to/images/directory
```

### Advanced Usage

#### Python API

```python
from detector import YOLODetector

# Initialize detector
detector = YOLODetector(
    model_name="yolov8m",
    conf_threshold=0.5,
    iou_threshold=0.45,
    device="cuda"  # or "cpu", "auto"
)

# Detect image
result = detector.detect_image(
    image_path="path/to/image.jpg",
    save_result=True,
    show_result=False,
    export_format="json"
)

print(f"Detected {result['num_detections']} objects")

# Detect video
video_result = detector.detect_video(
    video_path="path/to/video.mp4",
    save_result=True,
    export_format="both"
)

# Batch processing
batch_result = detector.detect_batch(
    input_dir="path/to/images",
    save_results=True,
    export_format="csv"
)

# Webcam detection
detector.detect_webcam(
    camera_id=0,
    show_result=True,
    save_result=False
)

# Benchmark performance
benchmark = detector.benchmark("path/to/test_image.jpg", num_runs=10)
print(f"Average FPS: {benchmark['fps']:.2f}")
```

#### Filter by Specific Classes

Detect only specific objects (e.g., person, car, dog):

```bash
python detector.py --input path/to/image.jpg --classes 0,2,16
```

**Class IDs (COCO dataset):**
- 0: person
- 1: bicycle
- 2: car
- 3: motorcycle
- 16: dog
- (See config.py for full list of 80 classes)

#### Custom Device Selection

Force CPU or GPU usage:

```bash
python detector.py --input path/to/image.jpg --device cpu
python detector.py --input path/to/image.jpg --device cuda
```

#### Export Formats

Choose export format for detection results:

```bash
python detector.py --input path/to/image.jpg --export json   # JSON format
python detector.py --input path/to/image.jpg --export csv    # CSV format
python detector.py --input path/to/image.jpg --export both  # Both formats
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input image/video/directory path | Required (unless --webcam) |
| `--model` | Model name (yolov8n, yolov8s, yolov8m, yolov8l, yolov8x) | yolov8m |
| `--conf` | Confidence threshold (0.0-1.0) | 0.25 |
| `--iou` | IOU threshold for NMS (0.0-1.0) | 0.45 |
| `--webcam` | Use webcam input | False |
| `--camera-id` | Webcam camera ID | 0 |
| `--show` | Show detection results | False |
| `--no-save` | Don't save results | False |
| `--export` | Export format (json, csv, both) | json |
| `--classes` | Comma-separated class IDs to detect | All classes |
| `--device` | Device (auto, cpu, cuda, mps) | auto |
| `--benchmark` | Run benchmark on image | False |

## Configuration

Edit `config.py` to customize default settings:

### Model Selection
```python
DEFAULT_MODEL = "yolov8m"  # Change default model
```

### Detection Parameters
```python
DETECTION_PARAMS = {
    "conf_threshold": 0.25,  # Adjust confidence threshold
    "iou_threshold": 0.45,   # Adjust IOU threshold
    "max_det": 300,          # Max detections per image
}
```

### Output Settings
```python
OUTPUT_SETTINGS = {
    "save_images": True,
    "save_videos": True,
    "show_confidence": True,
    "show_labels": True,
    "line_thickness": 2,
}
```

### Hardware Settings
```python
HARDWARE_SETTINGS = {
    "device": "auto",  # auto, cpu, cuda, mps
    "workers": 8,
    "batch_size": 16,
}
```

## Utility Functions

The `utils.py` module provides additional functions:

```python
from utils import (
    load_image, save_image, resize_image,
    draw_bbox, calculate_iou, non_max_suppression,
    filter_detections_by_class, filter_detections_by_confidence,
    get_detection_statistics, visualize_detections,
    plot_detection_statistics, extract_frames_from_video
)

# Load and process images
image = load_image("path/to/image.jpg")
resized = resize_image(image, (640, 640), keep_aspect_ratio=True)

# Filter detections
filtered = filter_detections_by_class(detections, ["person", "car"])
filtered = filter_detections_by_confidence(detections, 0.5)

# Get statistics
stats = get_detection_statistics(detections)
print(stats)

# Visualize
fig = visualize_detections(image, detections)
fig.savefig("visualization.png")

# Plot statistics
fig = plot_detection_statistics(detections)
fig.savefig("statistics.png")
```

## Model Comparison

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| YOLOv8-Nano | 640 | Very Fast | Medium | Edge devices, real-time |
| YOLOv8-Small | 640 | Fast | Good | Balanced performance |
| YOLOv8-Medium | 640 | Medium | High | General purpose |
| YOLOv8-Large | 640 | Slow | Very High | High accuracy needed |
| YOLOv8-XLarge | 640 | Very Slow | Highest | Maximum accuracy |

## Output Files

Detection results are saved in the `output/` directory:

- **Images**: `{filename}_detected.{ext}` - Annotated images
- **Videos**: `{filename}_detected.{ext}` - Annotated videos
- **JSON**: `{source}_detections_{timestamp}.json` - Structured detection data
- **CSV**: `{source}_detections_{timestamp}.csv` - Tabular detection data
- **Logs**: `detection.log` - Processing logs

## Troubleshooting

### Model Download Issues

If model download fails:
1. Check internet connection
2. Manually download model from Ultralytics hub
3. Place in `models/` directory with correct name (e.g., `yolov8m.pt`)

### CUDA Out of Memory

If you encounter GPU memory errors:
1. Use a smaller model (yolov8n or yolov8s)
2. Reduce batch size in config.py
3. Use CPU: `--device cpu`

### Slow Performance

To improve performance:
1. Use GPU if available: `--device cuda`
2. Use smaller model: `--model yolov8n`
3. Reduce image resolution
4. Increase confidence threshold to reduce detections

### Import Errors

If you get import errors:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Examples

### Example 1: Detect People in Image

```bash
python detector.py --input input/people.jpg --classes 0 --conf 0.6 --show
```

### Example 2: Process Video with High Confidence

```bash
python detector.py --input input/traffic.mp4 --conf 0.7 --model yolov8l
```

### Example 3: Batch Process Directory

```bash
python detector.py --input input/images/ --export both --model yolov8s
```

### Example 4: Webcam with Custom Settings

```bash
python detector.py --webcam --conf 0.5 --classes 0,2,3,5,7 --show
```

### Example 5: Benchmark Performance

```bash
python detector.py --input input/test.jpg --benchmark
```

## Performance Tips

1. **Use GPU**: Enable CUDA for 10-50x speedup
2. **Model Selection**: Choose appropriate model for your use case
3. **Batch Processing**: Process multiple images at once
4. **Confidence Threshold**: Higher threshold = faster processing
5. **Resolution**: Lower resolution = faster processing

## API Reference

### YOLODetector Class

#### Methods

- `detect_image(image_path, save_result, show_result, export_format)` - Detect objects in image
- `detect_video(video_path, save_result, show_result, export_format)` - Detect objects in video
- `detect_webcam(camera_id, show_result, save_result)` - Detect objects from webcam
- `detect_batch(input_dir, save_results, export_format)` - Batch process images
- `benchmark(image_path, num_runs)` - Benchmark detection performance
- `get_model_info()` - Get model information

## License

This project uses Ultralytics YOLOv8, which is licensed under AGPL-3.0. Please refer to the Ultralytics license for usage terms.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the Ultralytics documentation: https://docs.ultralytics.com/
3. Check the logs in `output/detection.log`

## Acknowledgments

- Ultralytics for YOLOv8 implementation
- COCO dataset for pretrained models
- OpenCV for image processing
- PyTorch for deep learning framework
