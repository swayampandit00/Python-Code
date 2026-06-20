"""
Utility functions for YOLO Object Detection
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns


def load_image(image_path: Union[str, Path]) -> np.ndarray:
    """Load image from path"""
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    return image


def save_image(image: np.ndarray, output_path: Union[str, Path]) -> None:
    """Save image to path"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), image)


def resize_image(
    image: np.ndarray,
    target_size: Tuple[int, int],
    keep_aspect_ratio: bool = True
) -> np.ndarray:
    """
    Resize image to target size
    
    Args:
        image: Input image
        target_size: Target size (width, height)
        keep_aspect_ratio: Whether to keep aspect ratio
        
    Returns:
        Resized image
    """
    if keep_aspect_ratio:
        h, w = image.shape[:2]
        target_w, target_h = target_size
        
        # Calculate scaling factor
        scale = min(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # Resize
        resized = cv2.resize(image, (new_w, new_h))
        
        # Create canvas
        canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        
        # Calculate padding
        pad_x = (target_w - new_w) // 2
        pad_y = (target_h - new_h) // 2
        
        # Place image on canvas
        canvas[pad_y:pad_y + new_h, pad_x:pad_x + new_w] = resized
        
        return canvas
    else:
        return cv2.resize(image, target_size)


def draw_bbox(
    image: np.ndarray,
    bbox: List[int],
    label: str = "",
    confidence: float = 0.0,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2,
    font_scale: float = 0.5
) -> np.ndarray:
    """
    Draw bounding box on image
    
    Args:
        image: Input image
        bbox: Bounding box [x1, y1, x2, y2]
        label: Label text
        confidence: Confidence score
        color: Box color (BGR)
        thickness: Line thickness
        font_scale: Font scale for label
        
    Returns:
        Image with drawn bounding box
    """
    x1, y1, x2, y2 = bbox
    
    # Draw box
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
    
    # Draw label
    if label:
        label_text = f"{label}"
        if confidence > 0:
            label_text += f" {confidence:.2f}"
        
        # Get label size
        (label_w, label_h), baseline = cv2.getTextSize(
            label_text,
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            thickness
        )
        
        # Draw label background
        cv2.rectangle(
            image,
            (x1, y1 - label_h - baseline - 5),
            (x1 + label_w, y1),
            color,
            -1
        )
        
        # Draw label text
        cv2.putText(
            image,
            label_text,
            (x1, y1 - baseline - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255),
            thickness
        )
    
    return image


def calculate_iou(bbox1: List[int], bbox2: List[int]) -> float:
    """
    Calculate Intersection over Union (IoU) between two bounding boxes
    
    Args:
        bbox1: First bounding box [x1, y1, x2, y2]
        bbox2: Second bounding box [x1, y1, x2, y2]
        
    Returns:
        IoU score
    """
    x1_1, y1_1, x2_1, y2_1 = bbox1
    x1_2, y1_2, x2_2, y2_2 = bbox2
    
    # Calculate intersection
    x1_i = max(x1_1, x1_2)
    y1_i = max(y1_1, y1_2)
    x2_i = min(x2_1, x2_2)
    y2_i = min(y2_1, y2_2)
    
    if x2_i <= x1_i or y2_i <= y1_i:
        return 0.0
    
    intersection = (x2_i - x1_i) * (y2_i - y1_i)
    
    # Calculate union
    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
    union = area1 + area2 - intersection
    
    if union == 0:
        return 0.0
    
    return intersection / union


def non_max_suppression(
    detections: List[Dict],
    iou_threshold: float = 0.45
) -> List[Dict]:
    """
    Apply Non-Maximum Suppression to detections
    
    Args:
        detections: List of detection dictionaries
        iou_threshold: IoU threshold for suppression
        
    Returns:
        Filtered detections
    """
    if not detections:
        return []
    
    # Sort by confidence (descending)
    detections = sorted(detections, key=lambda x: x["confidence"], reverse=True)
    
    keep = []
    while detections:
        # Keep the detection with highest confidence
        current = detections.pop(0)
        keep.append(current)
        
        # Remove detections with high IoU
        filtered = []
        for det in detections:
            iou = calculate_iou(
                [current["bbox"]["x1"], current["bbox"]["y1"], 
                 current["bbox"]["x2"], current["bbox"]["y2"]],
                [det["bbox"]["x1"], det["bbox"]["y1"], 
                 det["bbox"]["x2"], det["bbox"]["y2"]]
            )
            
            if iou < iou_threshold:
                filtered.append(det)
        
        detections = filtered
    
    return keep


def filter_detections_by_class(
    detections: List[Dict],
    class_names: List[str]
) -> List[Dict]:
    """
    Filter detections by class names
    
    Args:
        detections: List of detection dictionaries
        class_names: List of class names to keep
        
    Returns:
        Filtered detections
    """
    return [det for det in detections if det["class_name"] in class_names]


def filter_detections_by_confidence(
    detections: List[Dict],
    min_confidence: float
) -> List[Dict]:
    """
    Filter detections by minimum confidence
    
    Args:
        detections: List of detection dictionaries
        min_confidence: Minimum confidence threshold
        
    Returns:
        Filtered detections
    """
    return [det for det in detections if det["confidence"] >= min_confidence]


def filter_detections_by_area(
    detections: List[Dict],
    min_area: int = 0,
    max_area: int = float('inf')
) -> List[Dict]:
    """
    Filter detections by bounding box area
    
    Args:
        detections: List of detection dictionaries
        min_area: Minimum area
        max_area: Maximum area
        
    Returns:
        Filtered detections
    """
    return [
        det for det in detections 
        if min_area <= det["area"] <= max_area
    ]


def get_detection_statistics(detections: List[Dict]) -> Dict:
    """
    Calculate statistics from detections
    
    Args:
        detections: List of detection dictionaries
        
    Returns:
        Dictionary containing statistics
    """
    if not detections:
        return {
            "total_detections": 0,
            "unique_classes": 0,
            "class_counts": {},
            "avg_confidence": 0.0,
            "min_confidence": 0.0,
            "max_confidence": 0.0
        }
    
    # Count classes
    class_counts = {}
    for det in detections:
        class_name = det["class_name"]
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
    
    # Confidence statistics
    confidences = [det["confidence"] for det in detections]
    
    return {
        "total_detections": len(detections),
        "unique_classes": len(class_counts),
        "class_counts": class_counts,
        "avg_confidence": np.mean(confidences),
        "min_confidence": np.min(confidences),
        "max_confidence": np.max(confidences),
        "std_confidence": np.std(confidences)
    }


def visualize_detections(
    image: np.ndarray,
    detections: List[Dict],
    figsize: Tuple[int, int] = (12, 8)
) -> plt.Figure:
    """
    Visualize detections using matplotlib
    
    Args:
        image: Input image (BGR)
        detections: List of detection dictionaries
        figsize: Figure size
        
    Returns:
        Matplotlib figure
    """
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(image_rgb)
    
    for det in detections:
        bbox = det["bbox"]
        class_name = det["class_name"]
        confidence = det["confidence"]
        
        # Draw rectangle
        rect = Rectangle(
            (bbox["x1"], bbox["y1"]),
            bbox["width"],
            bbox["height"],
            linewidth=2,
            edgecolor='r',
            facecolor='none'
        )
        ax.add_patch(rect)
        
        # Add label
        ax.text(
            bbox["x1"],
            bbox["y1"] - 5,
            f"{class_name}: {confidence:.2f}",
            fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7)
        )
    
    ax.axis('off')
    ax.set_title(f'Detections: {len(detections)}')
    
    return fig


def plot_detection_statistics(
    detections: List[Dict],
    save_path: Optional[Union[str, Path]] = None
) -> plt.Figure:
    """
    Plot detection statistics
    
    Args:
        detections: List of detection dictionaries
        save_path: Path to save the plot
        
    Returns:
        Matplotlib figure
    """
    stats = get_detection_statistics(detections)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Class distribution
    if stats["class_counts"]:
        classes = list(stats["class_counts"].keys())
        counts = list(stats["class_counts"].values())
        
        axes[0, 0].bar(classes, counts)
        axes[0, 0].set_xlabel('Class')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].set_title('Class Distribution')
        axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Confidence distribution
    confidences = [det["confidence"] for det in detections]
    axes[0, 1].hist(confidences, bins=20, edgecolor='black')
    axes[0, 1].set_xlabel('Confidence')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Confidence Distribution')
    
    # Area distribution
    areas = [det["area"] for det in detections]
    axes[1, 0].hist(areas, bins=20, edgecolor='black')
    axes[1, 0].set_xlabel('Area (pixels)')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Bounding Box Area Distribution')
    
    # Summary statistics
    summary_text = f"""
    Total Detections: {stats['total_detections']}
    Unique Classes: {stats['unique_classes']}
    Avg Confidence: {stats['avg_confidence']:.4f}
    Min Confidence: {stats['min_confidence']:.4f}
    Max Confidence: {stats['max_confidence']:.4f}
    Std Confidence: {stats['std_confidence']:.4f}
    """
    axes[1, 1].text(0.1, 0.5, summary_text, fontsize=12, verticalalignment='center')
    axes[1, 1].axis('off')
    axes[1, 1].set_title('Summary Statistics')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_video_from_images(
    image_dir: Union[str, Path],
    output_path: Union[str, Path],
    fps: int = 30,
    pattern: str = "*.jpg"
) -> None:
    """
    Create video from images in a directory
    
    Args:
        image_dir: Directory containing images
        output_path: Output video path
        fps: Frames per second
        pattern: File pattern to match
    """
    image_dir = Path(image_dir)
    output_path = Path(output_path)
    
    # Get images
    images = sorted(image_dir.glob(pattern))
    if not images:
        raise ValueError(f"No images found matching pattern: {pattern}")
    
    # Read first image to get dimensions
    first_image = cv2.imread(str(images[0]))
    height, width = first_image.shape[:2]
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    # Write frames
    for image_path in images:
        image = cv2.imread(str(image_path))
        out.write(image)
    
    out.release()
    print(f"Video created: {output_path}")


def extract_frames_from_video(
    video_path: Union[str, Path],
    output_dir: Union[str, Path],
    frame_interval: int = 1,
    max_frames: Optional[int] = None
) -> List[Path]:
    """
    Extract frames from video
    
    Args:
        video_path: Input video path
        output_dir: Output directory for frames
        frame_interval: Extract every n-th frame
        max_frames: Maximum number of frames to extract
        
    Returns:
        List of extracted frame paths
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    
    frame_count = 0
    extracted_count = 0
    extracted_frames = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            frame_path = output_dir / f"frame_{frame_count:06d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            extracted_frames.append(frame_path)
            extracted_count += 1
            
            if max_frames and extracted_count >= max_frames:
                break
        
        frame_count += 1
    
    cap.release()
    print(f"Extracted {extracted_count} frames to {output_dir}")
    
    return extracted_frames


def merge_detections(
    detection_lists: List[List[Dict]]
) -> List[Dict]:
    """
    Merge multiple detection lists
    
    Args:
        detection_lists: List of detection lists
        
    Returns:
        Merged detection list
    """
    merged = []
    for detections in detection_lists:
        merged.extend(detections)
    return merged


def convert_bbox_format(
    bbox: Dict,
    from_format: str = "xyxy",
    to_format: str = "xywh"
) -> Dict:
    """
    Convert bounding box format
    
    Args:
        bbox: Bounding box dictionary
        from_format: Source format (xyxy, xywh)
        to_format: Target format (xyxy, xywh)
        
    Returns:
        Converted bounding box dictionary
    """
    if from_format == to_format:
        return bbox
    
    converted = bbox.copy()
    
    if from_format == "xyxy" and to_format == "xywh":
        converted["width"] = bbox["x2"] - bbox["x1"]
        converted["height"] = bbox["y2"] - bbox["y1"]
        converted["x"] = bbox["x1"]
        converted["y"] = bbox["y1"]
    elif from_format == "xywh" and to_format == "xyxy":
        converted["x1"] = bbox["x"]
        converted["y1"] = bbox["y"]
        converted["x2"] = bbox["x"] + bbox["width"]
        converted["y2"] = bbox["y"] + bbox["height"]
    
    return converted
