# Smart Attendance System

A Python-based face recognition attendance system using OpenCV. This system automatically detects faces, recognizes registered users, and marks their attendance in a CSV file.

## Features

- **Real-time Face Detection**: Uses webcam to detect faces in real-time
- **Face Recognition**: Trains on user faces and recognizes them during attendance
- **Automatic Attendance Marking**: Automatically marks attendance when recognized faces are detected
- **Attendance Management**: View, filter, and export attendance records
- **CSV/Excel Export**: Export attendance data to Excel for reporting
- **Graphical User Interface**: Modern GUI with tkinter for easy navigation
- **Single File Solution**: Unified application with all features in one file
- **EXE Creation**: Convert to standalone executable for distribution

## Requirements

- Python 3.8+
- Webcam
- Dependencies listed in `requirements.txt`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Unified Single File Application (Recommended)

Run the unified application that includes all features in one file:

```bash
python smart_attendance.py
```

This provides a menu-driven interface with all features:
- 📷 Collect Face Samples
- 🔄 Train Face Recognition Model
- 📹 Run Attendance System
- 👥 View Registered Users
- 📊 View All Attendance
- 📅 View Attendance by Date
- 👤 View Attendance by Person
- 📈 Generate Attendance Report
- 📤 Export to Excel

### Option 2: Graphical User Interface (GUI)

Run the modern GUI application with tkinter:

```bash
cd gui
python attendance_gui.py
```

The GUI provides:
- Modern dark theme interface
- Real-time camera preview
- One-click access to all features
- Visual attendance tracking
- Easy attendance management

### Option 3: Command Line Applications

#### Step 1: Train the Face Recognition Model

First, you need to train the model with face images of registered users.

**Option A: Collect face samples using webcam**
```bash
python train_faces.py
```
Select option 2, then enter the person's name and number of samples to collect (default 30). Press 's' to capture samples and 'q' to finish.

**Option B: Manually add face images**
1. Create a `faces` directory
2. Create subdirectories for each person (e.g., `faces/John/`, `faces/Jane/`)
3. Add face images (JPG/PNG) to each person's directory
4. Train the model:
```bash
python train_faces.py
```
Select option 3 to train the model from existing images.

#### Step 2: Run the Attendance System

```bash
python main.py
```

The system will:
- Open your webcam
- Detect faces in real-time
- Recognize registered users
- Automatically mark attendance in `attendance.csv`
- Display the name and confidence level on the video feed

Press 'q' to quit the system.

#### Step 3: Manage Attendance Records

```bash
python attendance_manager.py
```

Options:
1. View all attendance records
2. View attendance by date
3. View attendance by person
4. Generate attendance report
5. Export attendance to Excel

## Project Structure

```
smartAttendenceSystem/
├── smart_attendance.py     # Unified single-file application (Recommended)
├── main.py                 # Main attendance system with face detection
├── train_faces.py          # Face training module
├── attendance_manager.py   # Attendance record management
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── gui/                   # GUI application folder
│   ├── attendance_gui.py  # Graphical User Interface
│   ├── build_exe.spec     # PyInstaller configuration
│   └── BUILD_INSTRUCTIONS.md  # EXE build guide
├── faces/                 # Directory for face images (created during training)
├── trainer.yml            # Trained face recognition model
├── labels.pickle          # User labels mapping
└── attendance.csv         # Attendance records
```

## How It Works

1. **Face Detection**: Uses Haar Cascade classifier to detect faces in video frames
2. **Face Recognition**: Uses LBPH (Local Binary Patterns Histograms) algorithm for face recognition
3. **Attendance Marking**: When a face is recognized with sufficient confidence, attendance is marked
4. **Duplicate Prevention**: Each person can only mark attendance once per day

## Customization

- Adjust confidence threshold in `smart_attendance.py` (line 198)
- Change detection parameters in `smart_attendance.py` (line 191)
- Modify attendance file location in `smart_attendance.py` (line 17)

## Creating EXE File

To create a standalone executable for distribution:

### Prerequisites

```bash
pip install pyinstaller
```

### Build Process

1. **Navigate to gui folder**
```bash
cd gui
```

2. **Build EXE using spec file**
```bash
pyinstaller build_exe.spec
```

3. **The EXE will be created in** `dist/SmartAttendance.exe`

### Distribution

After building, you need to distribute these files together:
- `SmartAttendance.exe`
- `trainer.yml`
- `labels.pickle`
- `attendance.csv`
- `faces/` folder with all user data

For detailed instructions, see `gui/BUILD_INSTRUCTIONS.md`

## Troubleshooting

- **Webcam not opening**: Check if another application is using the webcam
- **Model not loading**: Ensure you've trained the model first using `train_faces.py` or the GUI
- **Poor recognition**: Collect more face samples with different angles and lighting conditions
- **OpenCV import error**: Ensure you've installed `opencv-contrib-python` (not just `opencv-python`)
- **GUI not opening**: Make sure tkinter is installed (usually included with Python)
- **EXE won't run**: Ensure all required files (trainer.yml, labels.pickle, attendance.csv, faces/) are in the same folder

## License

This project is open source and available for educational purposes.
