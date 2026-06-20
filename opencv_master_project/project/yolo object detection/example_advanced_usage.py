"""
Example: Advanced Usage of YOLO Detection
Demonstrates advanced features like filtering, statistics, and visualization
"""

from detector import YOLODetector
from utils import (
    filter_detections_by_class, filter_detections_by_confidence,
    filter_detections_by_area, get_detection_statistics,
    visualize_detections, plot_detection_statistics,
    non_max_suppression, calculate_iou
)
from pathlib import Path
import matplotlib.pyplot as plt


def example_filtering_detections():
    """Example of filtering detections"""
    print("=" * 50)
    print("Example 1: Filtering Detections")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8m")
    image_path = "input/test_image.jpg"
    
    try:
        result = detector.detect_image(
            image_path=image_path,
            save_result=False,
            show_result=False,
            export_format=None
        )
        
        detections = result['detections']
        print(f"Total detections: {len(detections)}")
        
        # Filter by class
        person_detections = filter_detections_by_class(detections, ["person"])
        print(f"Person detections: {len(person_detections)}")
        
        # Filter by confidence
        high_conf_detections = filter_detections_by_confidence(detections, 0.7)
        print(f"High confidence detections (>=0.7): {len(high_conf_detections)}")
        
        # Filter by area
        large_objects = filter_detections_by_area(detections, min_area=10000)
        print(f"Large objects (area >= 10000): {len(large_objects)}")
        
        # Combined filtering
        filtered = filter_detections_by_confidence(
            filter_detections_by_class(detections, ["person", "car"]),
            0.6
        )
        print(f"Person/Car with confidence >= 0.6: {len(filtered)}")
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def example_detection_statistics():
    """Example of calculating detection statistics"""
    print("\n" + "=" * 50)
    print("Example 2: Detection Statistics")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8m")
    image_path = "input/test_image.jpg"
    
    try:
        result = detector.detect_image(
            image_path=image_path,
            save_result=False,
            show_result=False,
            export_format=None
        )
        
        stats = get_detection_statistics(result['detections'])
        
        print(f"Total detections: {stats['total_detections']}")
        print(f"Unique classes: {stats['unique_classes']}")
        print(f"Average confidence: {stats['avg_confidence']:.4f}")
        print(f"Min confidence: {stats['min_confidence']:.4f}")
        print(f"Max confidence: {stats['max_confidence']:.4f}")
        print(f"Std confidence: {stats['std_confidence']:.4f}")
        
        print("\nClass counts:")
        for class_name, count in stats['class_counts'].items():
            print(f"  {class_name}: {count}")
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def example_visualization():
    """Example of visualizing detections with matplotlib"""
    print("\n" + "=" * 50)
    print("Example 3: Visualization")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8m")
    image_path = "input/test_image.jpg"
    
    try:
        # Load image
        import cv2
        image = cv2.imread(image_path)
        
        result = detector.detect_image(
            image_path=image_path,
            save_result=False,
            show_result=False,
            export_format=None
        )
        
        # Create visualization
        fig = visualize_detections(image, result['detections'])
        
        # Save visualization
        output_path = Path("output/visualization.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved to: {output_path}")
        
        plt.close(fig)
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def example_plot_statistics():
    """Example of plotting detection statistics"""
    print("\n" + "=" * 50)
    print("Example 4: Plot Statistics")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8m")
    image_path = "input/test_image.jpg"
    
    try:
        result = detector.detect_image(
            image_path=image_path,
            save_result=False,
            show_result=False,
            export_format=None
        )
        
        # Create statistics plot
        fig = plot_detection_statistics(
            result['detections'],
            save_path="output/statistics.png"
        )
        
        print(f"Statistics plot saved to: output/statistics.png")
        plt.close(fig)
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def example_iou_calculation():
    """Example of calculating IoU between bounding boxes"""
    print("\n" + "=" * 50)
    print("Example 5: IoU Calculation")
    print("=" * 50)
    
    # Example bounding boxes
    bbox1 = [100, 100, 200, 200]  # x1, y1, x2, y2
    bbox2 = [150, 150, 250, 250]
    bbox3 = [300, 300, 400, 400]  # No overlap
    
    iou_1_2 = calculate_iou(bbox1, bbox2)
    iou_1_3 = calculate_iou(bbox1, bbox3)
    
    print(f"IoU between bbox1 and bbox2 (overlapping): {iou_1_2:.4f}")
    print(f"IoU between bbox1 and bbox3 (no overlap): {iou_1_3:.4f}")


def example_nms():
    """Example of Non-Maximum Suppression"""
    print("\n" + "=" * 50)
    print("Example 6: Non-Maximum Suppression")
    print("=" * 50)
    
    # Create sample detections with overlapping boxes
    sample_detections = [
        {
            "class_name": "person",
            "confidence": 0.95,
            "bbox": {"x1": 100, "y1": 100, "x2": 200, "y2": 300, "width": 100, "height": 200, "center_x": 150, "center_y": 200},
            "area": 20000
        },
        {
            "class_name": "person",
            "confidence": 0.85,
            "bbox": {"x1": 110, "y1": 110, "x2": 210, "y2": 310, "width": 100, "height": 200, "center_x": 160, "center_y": 210},
            "area": 20000
        },
        {
            "class_name": "car",
            "confidence": 0.90,
            "bbox": {"x1": 300, "y1": 300, "x2": 500, "y2": 400, "width": 200, "height": 100, "center_x": 400, "center_y": 350},
            "area": 20000
        }
    ]
    
    print(f"Original detections: {len(sample_detections)}")
    
    # Apply NMS
    filtered = non_max_suppression(sample_detections, iou_threshold=0.5)
    
    print(f"After NMS: {len(filtered)}")
    print("Kept detections:")
    for det in filtered:
        print(f"  {det['class_name']}: {det['confidence']:.2f}")


def example_batch_analysis():
    """Example of analyzing batch detection results"""
    print("\n" + "=" * 50)
    print("Example 7: Batch Analysis")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8s")
    input_dir = "input"
    
    try:
        result = detector.detect_batch(
            input_dir=input_dir,
            save_results=True,
            export_format="json"
        )
        
        print(f"Batch processing complete!")
        print(f"Total images: {result['total_images']}")
        print(f"Total detections: {result['num_detections']}")
        
        # Analyze all detections
        stats = get_detection_statistics(result['all_detections'])
        
        print(f"\nOverall statistics:")
        print(f"Total detections: {stats['total_detections']}")
        print(f"Unique classes: {stats['unique_classes']}")
        print(f"Average confidence: {stats['avg_confidence']:.4f}")
        
        print("\nClass distribution:")
        for class_name, count in sorted(stats['class_counts'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {class_name}: {count}")
        
        # Create statistics plot
        fig = plot_detection_statistics(
            result['all_detections'],
            save_path="output/batch_statistics.png"
        )
        print(f"\nBatch statistics plot saved to: output/batch_statistics.png")
        plt.close(fig)
        
    except FileNotFoundError:
        print(f"Input directory not found: {input_dir}")


def example_custom_processing_pipeline():
    """Example of custom processing pipeline"""
    print("\n" + "=" * 50)
    print("Example 8: Custom Processing Pipeline")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8m")
    image_path = "input/test_image.jpg"
    
    try:
        # Step 1: Detect
        result = detector.detect_image(
            image_path=image_path,
            save_result=False,
            show_result=False,
            export_format=None
        )
        
        detections = result['detections']
        print(f"Step 1 - Initial detections: {len(detections)}")
        
        # Step 2: Filter by confidence
        detections = filter_detections_by_confidence(detections, 0.5)
        print(f"Step 2 - After confidence filter: {len(detections)}")
        
        # Step 3: Filter by class (keep only people and vehicles)
        vehicle_classes = ["person", "car", "truck", "bus", "motorcycle", "bicycle"]
        detections = filter_detections_by_class(detections, vehicle_classes)
        print(f"Step 3 - After class filter: {len(detections)}")
        
        # Step 4: Filter by size (remove very small objects)
        detections = filter_detections_by_area(detections, min_area=500)
        print(f"Step 4 - After area filter: {len(detections)}")
        
        # Step 5: Apply NMS
        detections = non_max_suppression(detections, iou_threshold=0.5)
        print(f"Step 5 - After NMS: {len(detections)}")
        
        # Step 6: Get final statistics
        stats = get_detection_statistics(detections)
        print(f"\nFinal statistics:")
        print(f"Total detections: {stats['total_detections']}")
        print(f"Classes found: {list(stats['class_counts'].keys())}")
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def example_model_info():
    """Example of getting model information"""
    print("\n" + "=" * 50)
    print("Example 9: Model Information")
    print("=" * 50)
    
    models = ["yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x"]
    
    for model_name in models:
        detector = YOLODetector(model_name=model_name)
        info = detector.get_model_info()
        
        print(f"\n{info['model_name']}:")
        print(f"  Device: {info['device']}")
        print(f"  Confidence threshold: {info['conf_threshold']}")
        print(f"  IOU threshold: {info['iou_threshold']}")
        print(f"  Max detections: {info['max_det']}")


def main():
    """Run all advanced examples"""
    print("YOLO Object Detection - Advanced Usage Examples")
    print("=" * 50)
    print("\nNote: Make sure to place test images in the 'input/' directory")
    print("Expected file: input/test_image.jpg")
    print("\nRunning examples...\n")
    
    # Run examples
    example_filtering_detections()
    example_detection_statistics()
    example_visualization()
    example_plot_statistics()
    example_iou_calculation()
    example_nms()
    example_batch_analysis()
    example_custom_processing_pipeline()
    example_model_info()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
