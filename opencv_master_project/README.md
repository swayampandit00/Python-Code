# OpenCV Master Project (Beginner)

Complete practical implementation from OpenCV PDF.

## Project Structure

```
opencv_master_project/
├── image_codes/
├── video_codes/
├── assets/
├── models/
├── haarcascade_files/
├── dataset/
├── project/
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Running Examples

Navigate to the respective directory and run the Python files:

```bash
# Image processing examples
cd image_codes
python read_image.py
python grayscale.py
python face_detection.py

# Video processing examples
cd video_codes
python webcam_capture.py
python video_grayscale.py
python face_detection_webcam.py
```

## Topics Covered

- **Image Processing**
  - Reading, displaying, and saving images
  - Grayscale conversion
  - Resizing, cropping, rotating, and flipping
  - Affine transformations and translation
  - Drawing shapes (lines, rectangles, circles, ellipses, polygons)
  - Text overlay
  - Color space conversions (BGR to RGB, HSV, Gray)

- **Color Detection**
  - Red color detection using HSV color space

- **Bitwise Operations**
  - AND, OR, XOR, NOT operations
  - Masking

- **Histogram**
  - Histogram calculation and visualization
  - Histogram equalization

- **Edge Detection**
  - Sobel edge detection
  - Laplacian edge detection
  - Canny edge detection

- **Face Detection & Recognition**
  - Face detection using Haar cascades
  - Eye detection
  - Face recognition using LBPH (Local Binary Patterns Histograms)
  - Live face recognition with webcam
  - Training custom face models

- **Video Processing**
  - Reading and displaying videos
  - Webcam capture
  - Video grayscale conversion
  - Video blur
  - Video edge detection
  - Frame extraction
  - Video properties (FPS, width, height)
  - Live text overlay
  - Motion detection
  - Basic object tracking

## Libraries Used

- **OpenCV** (opencv-python, opencv-contrib-python)
- **NumPy**
- **Matplotlib**

## File Structure

### image_codes/
```
image_codes/
├── affine_transformation.py
├── bgr_to_gray.py
├── bgr_to_hsv.py
├── bgr_to_rgb.py
├── bitwise_and.py
├── bitwise_not.py
├── bitwise_or.py
├── bitwise_xor.py
├── canny_edge.py
├── crop.py
├── draw_circle.py
├── draw_ellipse.py
├── draw_line.py
├── draw_polygon.py
├── draw_rectangle.py
├── face_detection.py
├── face_recognition.py
├── flip.py
├── grayscale.py
├── histogram.py
├── histogram_equalization.py
├── laplacian.py
├── live_face_recognize.py
├── masking.py
├── put_text.py
├── read_image.py
├── red_color_detection.py
├── resize.py
├── rotate.py
├── saveimage.py
├── show_image.py
├── sobel_edge.py
├── train_face_model.py
└── translate.py
```

### video_codes/
```
video_codes/
├── eye_detection.py
├── face_detection_webcam.py
├── frame_extraction.py
├── live_text_overlay.py
├── motion_detection.py
├── object_tracking_basic.py
├── read_video.py
├── real_time_face_recognition.py
├── video_blur.py
├── video_edge_detection.py
├── video_fps.py
├── video_grayscale.py
├── video_properties.py
├── webcam_capture.py
└── webcam_snapshot.py
```

### assets/
```
assets/
├── sample.jpg
├── person.jpg
└── sample.mp4
```

### models/
```
models/
├── face_model.yml
└── labels.txt
```

### haarcascade_files/
```
haarcascade_files/
├── haarcascade_frontalface_default.xml
└── haarcascade_eye.xml
```

### dataset/
```
dataset/
└── swayam/
    ├── 0.jpg
    ├── 1.jpg
    └── ... (50 images for face training)
```

## Notes

- All image processing scripts use relative paths to access assets from the `../assets/` directory
- All video processing scripts use relative paths to access videos from the `../assets/` directory
- Face recognition models are stored in the `../models/` directory
- To train a custom face model, run `train_face_model.py` from the `image_codes/` directory
- The project uses Haar cascade files for face and eye detection (loaded from OpenCV's built-in data)