"""
Example: Image Detection with YOLO
Demonstrates basic image detection with various options
"""

from detector import YOLODetector
from pathlib import Path
import cv2


def example_basic_detection():
    """Basic image detection example"""
    print("=" * 50)
    print("Example 1: Basic Image Detection")
    print("=" * 50)
    
    # Initialize detector
    detector = YOLODetector(model_name="yolov8m")
    
    # Detect objects in image
    image_path = "input/test_image.jpg"  # Replace with your image path
    
    try:
        result = detector.detect_image(
            image_path=image_path,
            save_result=True,
            show_result=False,
            export_format="json"
        )
        
        print(f"Detection complete!")
        print(f"Image: {result['image_path']}")
        print(f"Image shape: {result['image_shape']}")
        print(f"Number of detections: {result['num_detections']}")
        
        # Print first few detections
        for i, det in enumerate(result['detections'][:5]):
            print(f"  {i+1}. {det['class_name']}: {det['confidence']:.2f} at {det['bbox']}")
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")
        print("Please place a test image in the input/ directory")


def example_custom_thresholds():
    """Example with custom confidence and IOU thresholds"""
    print("\n" + "=" * 50)
    print("Example 2: Custom Thresholds")
    print("=" * 50)
    
    detector = YOLODetector(
        model_name="yolov8m",
        conf_threshold=0.6,  # Higher confidence threshold
        iou_threshold=0.4    # Lower IOU threshold
    )
    
    image_path = "input/test_image.jpg"
    
    try:
        result = detector.detect_image(
            image_path=image_path,
            save_result=True,
            export_format="json"
        )
        
        print(f"Detection with high confidence threshold (0.6)")
        print(f"Number of detections: {result['num_detections']}")
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def example_specific_classes():
    """Example detecting only specific classes (person, car, dog)"""
    print("\n" + "=" * 50)
    print("Example 3: Specific Classes Detection")
    print("=" * 50)
    
    # Class IDs: 0=person, 2=car, 16=dog
    detector = YOLODetector(
        model_name="yolov8m",
        classes=[0, 2, 16]
    )
    
    image_path = "input/test_image.jpg"
    
    try:
        result = detector.detect_image(
            image_path=image_path,
            save_result=True,
            export_format="json"
        )
        
        print(f"Detection for person, car, and dog only")
        print(f"Number of detections: {result['num_detections']}")
        
        # Show detected classes
        detected_classes = set(det['class_name'] for det in result['detections'])
        print(f"Detected classes: {detected_classes}")
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def example_multiple_images():
    """Example processing multiple images"""
    print("\n" + "=" * 50)
    print("Example 4: Batch Image Processing")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8s")
    
    input_dir = "input"  # Directory containing multiple images
    
    try:
        result = detector.detect_batch(
            input_dir=input_dir,
            save_results=True,
            export_format="both"
        )
        
        print(f"Batch processing complete!")
        print(f"Total images processed: {result['total_images']}")
        print(f"Total detections: {result['num_detections']}")
        
    except FileNotFoundError:
        print(f"Input directory not found: {input_dir}")


def example_show_result():
    """Example showing detection result on screen"""
    print("\n" + "=" * 50)
    print("Example 5: Show Detection Result")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8m")
    
    image_path = "input/test_image.jpg"
    
    try:
        result = detector.detect_image(
            image_path=image_path,
            save_result=True,
            show_result=True,  # This will display the image
            export_format="json"
        )
        
        print(f"Detection complete. Press any key to close the window.")
        
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def example_model_comparison():
    """Example comparing different model sizes"""
    print("\n" + "=" * 50)
    print("Example 6: Model Comparison")
    print("=" * 50)
    
    image_path = "input/test_image.jpg"
    models = ["yolov8n", "yolov8s", "yolov8m"]
    
    try:
        for model_name in models:
            print(f"\nTesting {model_name}...")
            detector = YOLODetector(model_name=model_name)
            
            result = detector.detect_image(
                image_path=image_path,
                save_result=False,
                show_result=False,
                export_format=None
            )
            
            print(f"  Detections: {result['num_detections']}")
            
            # Run benchmark
            benchmark = detector.benchmark(image_path, num_runs=5)
            print(f"  Average FPS: {benchmark['fps']:.2f}")
            print(f"  Mean time: {benchmark['mean_time']:.4f}s")
            
    except FileNotFoundError:
        print(f"Image not found: {image_path}")


def main():
    """Run all examples"""
    print("YOLO Object Detection - Image Examples")
    print("=" * 50)
    print("\nNote: Make sure to place test images in the 'input/' directory")
    print("Expected file: input/test_image.jpg")
    print("\nRunning examples...\n")
    
    # Run examples
    example_basic_detection()
    example_custom_thresholds()
    example_specific_classes()
    example_multiple_images()
    # example_show_result()  # Uncomment to enable GUI display
    example_model_comparison()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
