"""
Example: Webcam Detection with YOLO
Demonstrates real-time object detection from webcam
"""

from detector import YOLODetector
import cv2


def example_basic_webcam():
    """Basic webcam detection example"""
    print("=" * 50)
    print("Example 1: Basic Webcam Detection")
    print("=" * 50)
    print("Starting webcam detection...")
    print("Press 'q' to quit")
    
    detector = YOLODetector(
        model_name="yolov8s",  # Use smaller model for better FPS
        conf_threshold=0.5
    )
    
    try:
        detector.detect_webcam(
            camera_id=0,
            show_result=True,
            save_result=False
        )
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your webcam is connected and accessible")


def example_webcam_with_save():
    """Webcam detection with video saving"""
    print("\n" + "=" * 50)
    print("Example 2: Webcam Detection with Save")
    print("=" * 50)
    print("Starting webcam detection with recording...")
    print("Press 'q' to quit")
    print("Video will be saved to output/ directory")
    
    detector = YOLODetector(
        model_name="yolov8s",
        conf_threshold=0.5
    )
    
    try:
        detector.detect_webcam(
            camera_id=0,
            show_result=True,
            save_result=True
        )
    except Exception as e:
        print(f"Error: {e}")


def example_webcam_specific_classes():
    """Webcam detection for specific classes only"""
    print("\n" + "=" * 50)
    print("Example 3: Webcam Detection - Specific Classes")
    print("=" * 50)
    print("Detecting only: person, car, dog")
    print("Press 'q' to quit")
    
    detector = YOLODetector(
        model_name="yolov8s",
        classes=[0, 2, 16],  # person, car, dog
        conf_threshold=0.6
    )
    
    try:
        detector.detect_webcam(
            camera_id=0,
            show_result=True,
            save_result=False
        )
    except Exception as e:
        print(f"Error: {e}")


def example_webcam_high_performance():
    """Webcam detection optimized for performance"""
    print("\n" + "=" * 50)
    print("Example 4: Webcam Detection - High Performance")
    print("=" * 50)
    print("Using YOLOv8-Nano for maximum FPS")
    print("Press 'q' to quit")
    
    detector = YOLODetector(
        model_name="yolov8n",  # Smallest model for fastest inference
        conf_threshold=0.4
    )
    
    try:
        detector.detect_webcam(
            camera_id=0,
            show_result=True,
            save_result=False
        )
    except Exception as e:
        print(f"Error: {e}")


def example_webcam_high_accuracy():
    """Webcam detection optimized for accuracy"""
    print("\n" + "=" * 50)
    print("Example 5: Webcam Detection - High Accuracy")
    print("=" * 50)
    print("Using YOLOv8-Large for maximum accuracy")
    print("Note: This may have lower FPS")
    print("Press 'q' to quit")
    
    detector = YOLODetector(
        model_name="yolov8l",  # Large model for better accuracy
        conf_threshold=0.5
    )
    
    try:
        detector.detect_webcam(
            camera_id=0,
            show_result=True,
            save_result=False
        )
    except Exception as e:
        print(f"Error: {e}")


def example_webcam_multiple_cameras():
    """Example showing how to use different cameras"""
    print("\n" + "=" * 50)
    print("Example 6: Multiple Camera Selection")
    print("=" * 50)
    print("Available camera IDs usually: 0 (default), 1, 2, ...")
    print("To use a different camera, modify camera_id parameter")
    
    camera_id = input("Enter camera ID (default 0): ").strip()
    camera_id = int(camera_id) if camera_id else 0
    
    print(f"\nUsing camera {camera_id}")
    print("Press 'q' to quit")
    
    detector = YOLODetector(
        model_name="yolov8s",
        conf_threshold=0.5
    )
    
    try:
        detector.detect_webcam(
            camera_id=camera_id,
            show_result=True,
            save_result=False
        )
    except Exception as e:
        print(f"Error: {e}")
        print("Camera may not be available")


def example_webcam_with_custom_display():
    """Webcam detection with custom display settings"""
    print("\n" + "=" * 50)
    print("Example 7: Webcam Detection - Custom Display")
    print("=" * 50)
    print("Starting webcam with custom display...")
    print("Press 'q' to quit")
    
    from config import OUTPUT_SETTINGS
    
    # Customize display settings
    OUTPUT_SETTINGS["show_confidence"] = True
    OUTPUT_SETTINGS["show_labels"] = True
    OUTPUT_SETTINGS["line_thickness"] = 3
    OUTPUT_SETTINGS["font_size"] = 0.6
    
    detector = YOLODetector(
        model_name="yolov8s",
        conf_threshold=0.5
    )
    
    try:
        detector.detect_webcam(
            camera_id=0,
            show_result=True,
            save_result=False
        )
    except Exception as e:
        print(f"Error: {e}")


def list_available_cameras():
    """List available camera devices"""
    print("\n" + "=" * 50)
    print("Available Cameras")
    print("=" * 50)
    
    for i in range(5):  # Check first 5 camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera {i}: Available (Resolution: {frame.shape[1]}x{frame.shape[0]})")
            cap.release()
        else:
            print(f"Camera {i}: Not available")


def main():
    """Run webcam examples"""
    print("YOLO Object Detection - Webcam Examples")
    print("=" * 50)
    print("\nNote: Make sure your webcam is connected")
    print("\nRunning camera check...")
    list_available_cameras()
    
    print("\n" + "=" * 50)
    print("Select an example to run:")
    print("1. Basic webcam detection")
    print("2. Webcam with video saving")
    print("3. Webcam - specific classes (person, car, dog)")
    print("4. Webcam - high performance (YOLOv8-Nano)")
    print("5. Webcam - high accuracy (YOLOv8-Large)")
    print("6. Multiple camera selection")
    print("7. Custom display settings")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-7): ").strip()
    
    examples = {
        "1": example_basic_webcam,
        "2": example_webcam_with_save,
        "3": example_webcam_specific_classes,
        "4": example_webcam_high_performance,
        "5": example_webcam_high_accuracy,
        "6": example_webcam_multiple_cameras,
        "7": example_webcam_with_custom_display
    }
    
    if choice in examples:
        examples[choice]()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
