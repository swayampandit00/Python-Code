"""
Example: Video Detection with YOLO
Demonstrates video processing with various options
"""

from detector import YOLODetector
from pathlib import Path


def example_basic_video_detection():
    """Basic video detection example"""
    print("=" * 50)
    print("Example 1: Basic Video Detection")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8m")
    
    video_path = "input/test_video.mp4"  # Replace with your video path
    
    try:
        result = detector.detect_video(
            video_path=video_path,
            save_result=True,
            show_result=False,
            export_format="json"
        )
        
        print(f"Video processing complete!")
        print(f"Video: {result['video_path']}")
        print(f"Video shape: {result['video_shape']}")
        print(f"Total frames: {result['total_frames']}")
        print(f"FPS: {result['fps']}")
        print(f"Total detections: {result['num_detections']}")
        print(f"Output saved to: {result['output_path']}")
        
    except FileNotFoundError:
        print(f"Video not found: {video_path}")
        print("Please place a test video in the input/ directory")


def example_video_with_display():
    """Example showing video detection in real-time"""
    print("\n" + "=" * 50)
    print("Example 2: Video Detection with Display")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8s")  # Use smaller model for real-time
    
    video_path = "input/test_video.mp4"
    
    try:
        result = detector.detect_video(
            video_path=video_path,
            save_result=True,
            show_result=True,  # This will display the video
            export_format="json"
        )
        
        print(f"Video processing complete!")
        print(f"Total detections: {result['num_detections']}")
        
    except FileNotFoundError:
        print(f"Video not found: {video_path}")


def example_video_specific_classes():
    """Example detecting specific classes in video"""
    print("\n" + "=" * 50)
    print("Example 3: Video Detection - Specific Classes")
    print("=" * 50)
    
    # Detect only vehicles: car(2), truck(7), bus(5), motorcycle(3)
    detector = YOLODetector(
        model_name="yolov8m",
        classes=[2, 3, 5, 7]
    )
    
    video_path = "input/test_video.mp4"
    
    try:
        result = detector.detect_video(
            video_path=video_path,
            save_result=True,
            export_format="csv"
        )
        
        print(f"Vehicle detection complete!")
        print(f"Total vehicle detections: {result['num_detections']}")
        
    except FileNotFoundError:
        print(f"Video not found: {video_path}")


def example_video_high_confidence():
    """Example with high confidence threshold for cleaner results"""
    print("\n" + "=" * 50)
    print("Example 4: Video Detection - High Confidence")
    print("=" * 50)
    
    detector = YOLODetector(
        model_name="yolov8m",
        conf_threshold=0.7  # Only show detections with 70%+ confidence
    )
    
    video_path = "input/test_video.mp4"
    
    try:
        result = detector.detect_video(
            video_path=video_path,
            save_result=True,
            export_format="json"
        )
        
        print(f"High confidence detection complete!")
        print(f"Total detections (conf >= 0.7): {result['num_detections']}")
        
    except FileNotFoundError:
        print(f"Video not found: {video_path}")


def example_video_export_analysis():
    """Example with detailed export for analysis"""
    print("\n" + "=" * 50)
    print("Example 5: Video Detection - Detailed Export")
    print("=" * 50)
    
    detector = YOLODetector(model_name="yolov8m")
    
    video_path = "input/test_video.mp4"
    
    try:
        result = detector.detect_video(
            video_path=video_path,
            save_result=True,
            export_format="both"  # Export both JSON and CSV
        )
        
        print(f"Video processing complete!")
        print(f"Total detections: {result['num_detections']}")
        print(f"Results exported to JSON and CSV in output/ directory")
        
        # Analyze detections by class
        from collections import Counter
        class_counts = Counter(det['class_name'] for det in result['detections'])
        
        print("\nDetection summary by class:")
        for class_name, count in class_counts.most_common(10):
            print(f"  {class_name}: {count}")
        
    except FileNotFoundError:
        print(f"Video not found: {video_path}")


def example_video_skip_frames():
    """Example processing every Nth frame for faster processing"""
    print("\n" + "=" * 50)
    print("Example 6: Video Detection - Skip Frames")
    print("=" * 50)
    
    from config import VIDEO_SETTINGS
    
    # Process every 5th frame
    VIDEO_SETTINGS["skip_frames"] = 4  # Skip 4 frames, process 5th
    
    detector = YOLODetector(model_name="yolov8m")
    
    video_path = "input/test_video.mp4"
    
    try:
        result = detector.detect_video(
            video_path=video_path,
            save_result=True,
            export_format="json"
        )
        
        print(f"Frame-skipping detection complete!")
        print(f"Total frames: {result['total_frames']}")
        print(f"Total detections: {result['num_detections']}")
        
        # Reset skip frames
        VIDEO_SETTINGS["skip_frames"] = 0
        
    except FileNotFoundError:
        print(f"Video not found: {video_path}")


def main():
    """Run all examples"""
    print("YOLO Object Detection - Video Examples")
    print("=" * 50)
    print("\nNote: Make sure to place test videos in the 'input/' directory")
    print("Expected file: input/test_video.mp4")
    print("\nRunning examples...\n")
    
    # Run examples
    example_basic_video_detection()
    # example_video_with_display()  # Uncomment to enable GUI display
    example_video_specific_classes()
    example_video_high_confidence()
    example_video_export_analysis()
    example_video_skip_frames()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
