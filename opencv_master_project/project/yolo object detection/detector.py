"""
Advanced YOLO Object Detection Module
Supports image, video, webcam, and batch processing with tracking and export capabilities
"""

import cv2
import numpy as np
import json
import csv
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
from datetime import datetime
import torch
from ultralytics import YOLO
from tqdm import tqdm
import pandas as pd

from config import (
    MODEL_CONFIGS, DEFAULT_MODEL, DETECTION_PARAMS, COCO_CLASSES,
    OUTPUT_SETTINGS, VIDEO_SETTINGS, TRACKING_SETTINGS, 
    HARDWARE_SETTINGS, LOGGING_SETTINGS, OUTPUT_DIR, MODELS_DIR
)


class YOLODetector:
    """Advanced YOLO Object Detection Class"""
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: str = None,
        conf_threshold: float = None,
        iou_threshold: float = None,
        max_det: int = None,
        classes: List[int] = None,
        tracking: bool = False
    ):
        """
        Initialize YOLO Detector
        
        Args:
            model_name: Model name (yolov8n, yolov8s, yolov8m, yolov8l, yolov8x)
            device: Device to run inference on (auto, cpu, cuda, mps)
            conf_threshold: Confidence threshold for detections
            iou_threshold: IOU threshold for NMS
            max_det: Maximum number of detections per image
            classes: List of class IDs to detect (None for all)
            tracking: Enable object tracking
        """
        self.model_name = model_name
        self.device = self._get_device(device)
        self.conf_threshold = conf_threshold or DETECTION_PARAMS["conf_threshold"]
        self.iou_threshold = iou_threshold or DETECTION_PARAMS["iou_threshold"]
        self.max_det = max_det or DETECTION_PARAMS["max_det"]
        self.classes = classes
        self.tracking = tracking
        
        self.model = None
        self.class_names = COCO_CLASSES
        self.colors = self._generate_colors()
        
        self._setup_logging()
        self._load_model()
        
    def _get_device(self, device: str) -> str:
        """Determine the best device to use"""
        if device:
            return device
        
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_level = getattr(logging, LOGGING_SETTINGS["level"])
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOGGING_SETTINGS["log_file"]),
                logging.StreamHandler() if LOGGING_SETTINGS["console_output"] else None
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_model(self):
        """Load YOLO model"""
        try:
            model_path = MODELS_DIR / f"{self.model_name}.pt"
            
            if not model_path.exists():
                self.logger.info(f"Model not found locally. Downloading {self.model_name}...")
                model_url = MODEL_CONFIGS[self.model_name]["url"]
                self.model = YOLO(model_url)
                # Save model locally
                self.model.save(str(model_path))
            else:
                self.logger.info(f"Loading model from {model_path}")
                self.model = YOLO(str(model_path))
            
            self.model.to(self.device)
            self.logger.info(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            raise
    
    def _generate_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Generate colors for each class"""
        colors = {}
        np.random.seed(42)
        for class_name in self.class_names:
            colors[class_name] = tuple(np.random.randint(0, 255, 3).tolist())
        return colors
    
    def detect_image(
        self,
        image_path: Union[str, Path],
        save_result: bool = True,
        show_result: bool = False,
        export_format: str = "json"
    ) -> Dict:
        """
        Detect objects in a single image
        
        Args:
            image_path: Path to input image
            save_result: Save the result image
            show_result: Display the result image
            export_format: Export format (json, csv, both)
            
        Returns:
            Dictionary containing detection results
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        self.logger.info(f"Processing image: {image_path}")
        
        # Read image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Run detection
        results = self.model(
            image,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            max_det=self.max_det,
            classes=self.classes,
            device=self.device,
            verbose=False
        )
        
        # Process results
        detections = self._process_results(results[0], image.shape)
        
        # Draw detections
        if OUTPUT_SETTINGS["save_images"] or show_result:
            annotated_image = self._draw_detections(image, detections)
            
            if save_result:
                output_path = OUTPUT_DIR / f"{image_path.stem}_detected{image_path.suffix}"
                cv2.imwrite(str(output_path), annotated_image)
                self.logger.info(f"Result saved to: {output_path}")
            
            if show_result:
                cv2.imshow("Detection Result", annotated_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        
        # Export results
        if export_format:
            self._export_results(detections, image_path, export_format)
        
        return {
            "image_path": str(image_path),
            "image_shape": image.shape,
            "detections": detections,
            "num_detections": len(detections)
        }
    
    def detect_video(
        self,
        video_path: Union[str, Path],
        save_result: bool = True,
        show_result: bool = False,
        export_format: str = "json"
    ) -> Dict:
        """
        Detect objects in a video
        
        Args:
            video_path: Path to input video
            save_result: Save the result video
            show_result: Display the result video
            export_format: Export format (json, csv, both)
            
        Returns:
            Dictionary containing detection results
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        self.logger.info(f"Processing video: {video_path}")
        
        # Open video
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Setup video writer
        output_path = None
        if save_result:
            output_path = OUTPUT_DIR / f"{video_path.stem}_detected{video_path.suffix}"
            fourcc = cv2.VideoWriter_fourcc(*VIDEO_SETTINGS["fourcc"])
            out = cv2.VideoWriter(
                str(output_path),
                fourcc,
                fps,
                (width, height)
            )
        
        # Process frames
        all_detections = []
        frame_count = 0
        
        with tqdm(total=total_frames, desc="Processing frames") as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Skip frames if configured
                if VIDEO_SETTINGS["skip_frames"] > 0 and frame_count % (VIDEO_SETTINGS["skip_frames"] + 1) != 0:
                    continue
                
                # Run detection
                results = self.model(
                    frame,
                    conf=self.conf_threshold,
                    iou=self.iou_threshold,
                    max_det=self.max_det,
                    classes=self.classes,
                    device=self.device,
                    verbose=False
                )
                
                # Process results
                detections = self._process_results(results[0], frame.shape, frame_count)
                all_detections.extend(detections)
                
                # Draw detections
                annotated_frame = self._draw_detections(frame, detections)
                
                # Write frame
                if save_result:
                    out.write(annotated_frame)
                
                # Show frame
                if show_result:
                    cv2.imshow("Video Detection", annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                pbar.update(1)
        
        # Cleanup
        cap.release()
        if save_result:
            out.release()
        cv2.destroyAllWindows()
        
        # Export results
        if export_format:
            self._export_results(all_detections, video_path, export_format)
        
        self.logger.info(f"Video processing complete. Total frames: {frame_count}")
        
        return {
            "video_path": str(video_path),
            "video_shape": (height, width),
            "total_frames": frame_count,
            "fps": fps,
            "detections": all_detections,
            "num_detections": len(all_detections),
            "output_path": str(output_path) if output_path else None
        }
    
    def detect_webcam(
        self,
        camera_id: int = 0,
        show_result: bool = True,
        save_result: bool = False
    ):
        """
        Detect objects from webcam stream
        
        Args:
            camera_id: Camera device ID
            show_result: Display the result
            save_result: Save the result video
        """
        self.logger.info(f"Starting webcam detection on camera {camera_id}")
        
        # Open webcam
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            raise ValueError(f"Could not open webcam: {camera_id}")
        
        # Setup video writer if saving
        output_path = None
        if save_result:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"webcam_{timestamp}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*VIDEO_SETTINGS["fourcc"])
            fps = 30
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Run detection
                results = self.model(
                    frame,
                    conf=self.conf_threshold,
                    iou=self.iou_threshold,
                    max_det=self.max_det,
                    classes=self.classes,
                    device=self.device,
                    verbose=False
                )
                
                # Process results
                detections = self._process_results(results[0], frame.shape, frame_count)
                
                # Draw detections
                annotated_frame = self._draw_detections(frame, detections)
                
                # Add frame info
                cv2.putText(
                    annotated_frame,
                    f"Frame: {frame_count} | Objects: {len(detections)}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                # Write frame
                if save_result:
                    out.write(annotated_frame)
                
                # Show frame
                if show_result:
                    cv2.imshow("Webcam Detection", annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        
        except KeyboardInterrupt:
            self.logger.info("Webcam detection stopped by user")
        
        finally:
            cap.release()
            if save_result:
                out.release()
            cv2.destroyAllWindows()
            self.logger.info(f"Webcam detection complete. Total frames: {frame_count}")
    
    def detect_batch(
        self,
        input_dir: Union[str, Path],
        save_results: bool = True,
        export_format: str = "json"
    ) -> Dict:
        """
        Detect objects in multiple images (batch processing)
        
        Args:
            input_dir: Directory containing images
            save_results: Save result images
            export_format: Export format (json, csv, both)
            
        Returns:
            Dictionary containing all detection results
        """
        input_dir = Path(input_dir)
        if not input_dir.exists():
            raise FileNotFoundError(f"Directory not found: {input_dir}")
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(input_dir.glob(f"*{ext}"))
            image_files.extend(input_dir.glob(f"*{ext.upper()}"))
        
        if not image_files:
            self.logger.warning(f"No images found in {input_dir}")
            return {"total_images": 0, "all_detections": []}
        
        self.logger.info(f"Processing {len(image_files)} images in batch")
        
        all_detections = []
        
        for image_path in tqdm(image_files, desc="Batch processing"):
            try:
                result = self.detect_image(
                    image_path,
                    save_result=save_results,
                    show_result=False,
                    export_format=None  # Export at the end
                )
                all_detections.extend(result["detections"])
            except Exception as e:
                self.logger.error(f"Error processing {image_path}: {e}")
        
        # Export all results
        if export_format:
            self._export_results(all_detections, input_dir, export_format, is_batch=True)
        
        return {
            "input_dir": str(input_dir),
            "total_images": len(image_files),
            "all_detections": all_detections,
            "num_detections": len(all_detections)
        }
    
    def _process_results(
        self,
        result,
        image_shape: Tuple[int, int, int],
        frame_number: int = None
    ) -> List[Dict]:
        """Process YOLO results into structured format"""
        detections = []
        
        if result.boxes is None:
            return detections
        
        boxes = result.boxes
        
        for i in range(len(boxes)):
            box = boxes.xyxy[i].cpu().numpy()  # x1, y1, x2, y2
            conf = float(boxes.conf[i].cpu().numpy())
            class_id = int(boxes.cls[i].cpu().numpy())
            
            x1, y1, x2, y2 = map(int, box)
            width = x2 - x1
            height = y2 - y1
            center_x = x1 + width // 2
            center_y = y1 + height // 2
            
            detection = {
                "class_id": class_id,
                "class_name": self.class_names[class_id] if class_id < len(self.class_names) else f"class_{class_id}",
                "confidence": round(conf, 4),
                "bbox": {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "width": width,
                    "height": height,
                    "center_x": center_x,
                    "center_y": center_y
                },
                "area": width * height
            }
            
            if frame_number is not None:
                detection["frame_number"] = frame_number
            
            detections.append(detection)
        
        return detections
    
    def _draw_detections(
        self,
        image: np.ndarray,
        detections: List[Dict]
    ) -> np.ndarray:
        """Draw detection boxes and labels on image"""
        annotated = image.copy()
        
        for det in detections:
            class_name = det["class_name"]
            confidence = det["confidence"]
            bbox = det["bbox"]
            
            # Get color
            color = self.colors.get(class_name, (0, 255, 0))
            
            # Draw box
            cv2.rectangle(
                annotated,
                (bbox["x1"], bbox["y1"]),
                (bbox["x2"], bbox["y2"]),
                color,
                OUTPUT_SETTINGS["line_thickness"]
            )
            
            # Draw label
            if OUTPUT_SETTINGS["show_labels"]:
                label = f"{class_name}"
                if OUTPUT_SETTINGS["show_confidence"]:
                    label += f" {confidence:.2f}"
                
                # Get label size
                (label_width, label_height), baseline = cv2.getTextSize(
                    label,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    OUTPUT_SETTINGS["font_size"],
                    OUTPUT_SETTINGS["line_thickness"]
                )
                
                # Draw label background
                cv2.rectangle(
                    annotated,
                    (bbox["x1"], bbox["y1"] - label_height - baseline - 5),
                    (bbox["x1"] + label_width, bbox["y1"]),
                    color,
                    -1
                )
                
                # Draw label text
                cv2.putText(
                    annotated,
                    label,
                    (bbox["x1"], bbox["y1"] - baseline - 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    OUTPUT_SETTINGS["font_size"],
                    (255, 255, 255),
                    OUTPUT_SETTINGS["line_thickness"]
                )
        
        return annotated
    
    def _export_results(
        self,
        detections: List[Dict],
        source: Union[str, Path],
        export_format: str,
        is_batch: bool = False
    ):
        """Export detection results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source_name = Path(source).stem if not is_batch else "batch"
        
        if export_format in ["json", "both"]:
            json_path = OUTPUT_DIR / f"{source_name}_detections_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(detections, f, indent=2)
            self.logger.info(f"Results exported to JSON: {json_path}")
        
        if export_format in ["csv", "both"]:
            csv_path = OUTPUT_DIR / f"{source_name}_detections_{timestamp}.csv"
            
            # Flatten detections for CSV
            flattened = []
            for det in detections:
                flat_det = {
                    "class_id": det["class_id"],
                    "class_name": det["class_name"],
                    "confidence": det["confidence"],
                    "x1": det["bbox"]["x1"],
                    "y1": det["bbox"]["y1"],
                    "x2": det["bbox"]["x2"],
                    "y2": det["bbox"]["y2"],
                    "width": det["bbox"]["width"],
                    "height": det["bbox"]["height"],
                    "center_x": det["bbox"]["center_x"],
                    "center_y": det["bbox"]["center_y"],
                    "area": det["area"]
                }
                if "frame_number" in det:
                    flat_det["frame_number"] = det["frame_number"]
                flattened.append(flat_det)
            
            df = pd.DataFrame(flattened)
            df.to_csv(csv_path, index=False)
            self.logger.info(f"Results exported to CSV: {csv_path}")
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "model_info": MODEL_CONFIGS[self.model_name],
            "device": self.device,
            "conf_threshold": self.conf_threshold,
            "iou_threshold": self.iou_threshold,
            "max_det": self.max_det,
            "classes": self.classes,
            "tracking": self.tracking,
            "num_classes": len(self.class_names)
        }
    
    def benchmark(self, image_path: Union[str, Path], num_runs: int = 10) -> Dict:
        """
        Benchmark detection performance
        
        Args:
            image_path: Path to test image
            num_runs: Number of benchmark runs
            
        Returns:
            Dictionary containing benchmark results
        """
        import time
        
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        self.logger.info(f"Running benchmark with {num_runs} iterations")
        
        times = []
        
        # Warmup
        for _ in range(3):
            self.model(image, verbose=False)
        
        # Benchmark
        for _ in range(num_runs):
            start_time = time.time()
            self.model(image, verbose=False)
            end_time = time.time()
            times.append(end_time - start_time)
        
        times = np.array(times)
        
        results = {
            "num_runs": num_runs,
            "mean_time": float(np.mean(times)),
            "std_time": float(np.std(times)),
            "min_time": float(np.min(times)),
            "max_time": float(np.max(times)),
            "fps": 1.0 / np.mean(times),
            "image_shape": image.shape
        }
        
        self.logger.info(f"Benchmark complete. Average FPS: {results['fps']:.2f}")
        
        return results


def main():
    """Example usage of YOLODetector"""
    import argparse
    
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, help="Input image/video/directory path")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, 
                       choices=list(MODEL_CONFIGS.keys()), help="Model name")
    parser.add_argument("--conf", type=float, default=DETECTION_PARAMS["conf_threshold"],
                       help="Confidence threshold")
    parser.add_argument("--iou", type=float, default=DETECTION_PARAMS["iou_threshold"],
                       help="IOU threshold")
    parser.add_argument("--webcam", action="store_true", help="Use webcam")
    parser.add_argument("--camera-id", type=int, default=0, help="Webcam camera ID")
    parser.add_argument("--show", action="store_true", help="Show results")
    parser.add_argument("--no-save", action="store_true", help="Don't save results")
    parser.add_argument("--export", type=str, default="json", choices=["json", "csv", "both"],
                       help="Export format")
    parser.add_argument("--classes", type=str, help="Comma-separated class IDs to detect")
    parser.add_argument("--device", type=str, help="Device (auto, cpu, cuda, mps)")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark")
    
    args = parser.parse_args()
    
    # Parse classes
    classes = None
    if args.classes:
        classes = [int(c.strip()) for c in args.classes.split(",")]
    
    # Initialize detector
    detector = YOLODetector(
        model_name=args.model,
        device=args.device,
        conf_threshold=args.conf,
        iou_threshold=args.iou,
        classes=classes
    )
    
    print(f"Model Info: {detector.get_model_info()}")
    
    # Run detection
    if args.webcam:
        detector.detect_webcam(
            camera_id=args.camera_id,
            show_result=args.show,
            save_result=not args.no_save
        )
    elif args.input:
        input_path = Path(args.input)
        
        if input_path.is_dir():
            results = detector.detect_batch(
                input_path,
                save_results=not args.no_save,
                export_format=args.export
            )
        elif input_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
            results = detector.detect_video(
                input_path,
                save_result=not args.no_save,
                show_result=args.show,
                export_format=args.export
            )
        else:
            results = detector.detect_image(
                input_path,
                save_result=not args.no_save,
                show_result=args.show,
                export_format=args.export
            )
        
        print(f"Detection complete. Total detections: {results['num_detections']}")
        
        if args.benchmark and input_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            benchmark_results = detector.benchmark(input_path)
            print(f"Benchmark Results: {benchmark_results}")
    else:
        print("Please provide --input or use --webcam")


if __name__ == "__main__":
    main()
