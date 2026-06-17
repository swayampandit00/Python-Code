import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime
import pickle
import sys

class SmartAttendanceSystem:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {}
        self.label_ids = {}
        self.current_id = 0
        self.faces_dir = 'faces'
        self.attendance_file = 'attendance.csv'
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize all necessary directories and files"""
        # Create faces directory
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
            print(f"✓ Created '{self.faces_dir}' directory")
        
        # Create attendance file
        if not os.path.exists(self.attendance_file):
            df = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Status'])
            df.to_csv(self.attendance_file, index=False)
            print(f"✓ Created '{self.attendance_file}' file")
        
        # Load trained model if exists
        if os.path.exists('trainer.yml') and os.path.exists('labels.pickle'):
            self.recognizer.read('trainer.yml')
            with open('labels.pickle', 'rb') as f:
                self.labels = pickle.load(f)
            self.labels = {v: k for k, v in self.labels.items()}
            print(f"✓ Loaded trained model with {len(self.labels)} users")
        else:
            print("⚠ No trained model found. Please train the model first.")
    
    def collect_face_samples(self, person_name, num_samples=30):
        """Collect face samples from webcam for a person"""
        person_dir = os.path.join(self.faces_dir, person_name)
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return False
        
        print(f"\n📷 Collecting {num_samples} face samples for {person_name}")
        print("   Press 's' to capture a sample, 'q' to finish")
        
        sample_count = 0
        
        while sample_count < num_samples:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read frame")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, f"Samples: {sample_count}/{num_samples}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow('Face Collection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s') and len(faces) > 0:
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    sample_path = os.path.join(person_dir, f"{person_name}_{sample_count}.jpg")
                    cv2.imwrite(sample_path, face_roi)
                    print(f"   ✓ Saved sample {sample_count + 1}")
                    sample_count += 1
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"✓ Collected {sample_count} samples for {person_name}")
        return sample_count > 0
    
    def train_model(self):
        """Train the face recognition model from collected face images"""
        print("\n🔄 Training face recognition model...")
        
        face_samples = []
        ids = []
        self.label_ids = {}
        self.current_id = 0
        
        # Iterate through each person's directory
        for root, dirs, files in os.walk(self.faces_dir):
            for file in files:
                if file.endswith("jpg") or file.endswith("png"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root)
                    
                    # Assign ID to label
                    if label not in self.label_ids:
                        self.label_ids[label] = self.current_id
                        self.current_id += 1
                    
                    id_ = self.label_ids[label]
                    
                    # Read and process image
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        face_samples.append(img)
                        ids.append(id_)
        
        if len(face_samples) == 0:
            print("❌ No face images found in the faces directory")
            return False
        
        # Train the recognizer
        self.recognizer.train(face_samples, np.array(ids))
        
        # Save the trained model
        self.recognizer.save('trainer.yml')
        
        # Save the labels
        with open('labels.pickle', 'wb') as f:
            pickle.dump(self.label_ids, f)
        
        # Reload labels
        self.labels = {v: k for k, v in self.label_ids.items()}
        
        print(f"✓ Training completed! Model saved as 'trainer.yml'")
        print(f"✓ Trained on {len(face_samples)} face images")
        print(f"✓ Users: {list(self.label_ids.keys())}")
        return True
    
    def mark_attendance(self, name):
        """Mark attendance for the recognized person"""
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        
        # Read existing attendance
        df = pd.read_csv(self.attendance_file)
        
        # Check if person already marked attendance today
        today_attendance = df[(df['Name'] == name) & (df['Date'] == date)]
        
        if today_attendance.empty:
            # Mark new attendance
            new_entry = pd.DataFrame([[name, date, time, 'Present']], 
                                    columns=['Name', 'Date', 'Time', 'Status'])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(self.attendance_file, index=False)
            print(f"✓ Attendance marked for {name} at {time}")
            return True
        else:
            return False
    
    def run_attendance_system(self):
        """Run the real-time attendance system"""
        if not os.path.exists('trainer.yml'):
            print("❌ No trained model found. Please train the model first.")
            return
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return
        
        print("\n📹 Running attendance system...")
        print("   Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read frame")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            
            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                
                # Recognize the face
                id_, confidence = self.recognizer.predict(face_roi)
                
                if confidence < 100:
                    name = self.labels.get(id_, "Unknown")
                    confidence = f"{100 - confidence:.0f}%"
                    color = (0, 255, 0)
                    
                    # Mark attendance
                    self.mark_attendance(name)
                else:
                    name = "Unknown"
                    confidence = f"{100 - confidence:.0f}%"
                    color = (0, 0, 255)
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # Draw label
                cv2.putText(frame, f"{name} ({confidence})", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            cv2.imshow('Smart Attendance System', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("✓ Attendance system stopped")
    
    def view_all_attendance(self):
        """View all attendance records"""
        df = pd.read_csv(self.attendance_file)
        print("\n📊 All Attendance Records:")
        print(df.to_string(index=False))
    
    def view_attendance_by_date(self, date):
        """View attendance records for a specific date"""
        df = pd.read_csv(self.attendance_file)
        result = df[df['Date'] == date]
        print(f"\n📊 Attendance for {date}:")
        print(result.to_string(index=False))
    
    def view_attendance_by_person(self, name):
        """View all attendance records for a specific person"""
        df = pd.read_csv(self.attendance_file)
        result = df[df['Name'] == name]
        print(f"\n📊 Attendance for {name}:")
        print(result.to_string(index=False))
    
    def generate_report(self, start_date=None, end_date=None):
        """Generate attendance report for a date range"""
        df = pd.read_csv(self.attendance_file)
        
        if start_date:
            df = df[df['Date'] >= start_date]
        if end_date:
            df = df[df['Date'] <= end_date]
        
        total_records = len(df)
        unique_persons = df['Name'].nunique()
        
        print(f"\n📈 Attendance Report")
        print(f"   Date Range: {start_date} to {end_date}")
        print(f"   Total Records: {total_records}")
        print(f"   Unique Persons: {unique_persons}")
        print(f"\n   Attendance by Person:")
        
        person_stats = df.groupby('Name').size().reset_index(name='Days Present')
        print(person_stats.to_string(index=False))
    
    def export_to_excel(self, output_file='attendance_report.xlsx'):
        """Export attendance data to Excel file"""
        try:
            df = pd.read_csv(self.attendance_file)
            df.to_excel(output_file, index=False)
            print(f"✓ Attendance data exported to {output_file}")
        except ImportError:
            print("❌ openpyxl not installed. Install it with: pip install openpyxl")
    
    def list_registered_users(self):
        """List all registered users"""
        if os.path.exists('labels.pickle'):
            with open('labels.pickle', 'rb') as f:
                self.label_ids = pickle.load(f)
            print(f"\n👥 Registered Users ({len(self.label_ids)}):")
            for name, id_ in self.label_ids.items():
                print(f"   - {name}")
        else:
            print("\n⚠ No users registered yet")
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("     SMART ATTENDANCE SYSTEM")
        print("="*50)
        print("1. 📷 Collect Face Samples")
        print("2. 🔄 Train Face Recognition Model")
        print("3. 📹 Run Attendance System")
        print("4. 👥 View Registered Users")
        print("5. 📊 View All Attendance")
        print("6. 📅 View Attendance by Date")
        print("7. 👤 View Attendance by Person")
        print("8. 📈 Generate Attendance Report")
        print("9. 📤 Export to Excel")
        print("0. ❌ Exit")
        print("="*50)
    
    def run(self):
        """Run the main application"""
        print("\n🚀 Smart Attendance System Initialized")
        
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == '0':
                print("\n👋 Thank you for using Smart Attendance System!")
                break
            
            elif choice == '1':
                name = input("Enter person's name: ").strip()
                if name:
                    num_samples = input("Enter number of samples (default 30): ").strip()
                    num_samples = int(num_samples) if num_samples else 30
                    self.collect_face_samples(name, num_samples)
                else:
                    print("❌ Name cannot be empty")
            
            elif choice == '2':
                self.train_model()
            
            elif choice == '3':
                self.run_attendance_system()
            
            elif choice == '4':
                self.list_registered_users()
            
            elif choice == '5':
                self.view_all_attendance()
            
            elif choice == '6':
                date = input("Enter date (YYYY-MM-DD): ").strip()
                if date:
                    self.view_attendance_by_date(date)
                else:
                    print("❌ Date cannot be empty")
            
            elif choice == '7':
                name = input("Enter person's name: ").strip()
                if name:
                    self.view_attendance_by_person(name)
                else:
                    print("❌ Name cannot be empty")
            
            elif choice == '8':
                start_date = input("Enter start date (YYYY-MM-DD, leave blank for all): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD, leave blank for all): ").strip()
                self.generate_report(start_date if start_date else None, end_date if end_date else None)
            
            elif choice == '9':
                output_file = input("Enter output filename (default: attendance_report.xlsx): ").strip()
                self.export_to_excel(output_file if output_file else 'attendance_report.xlsx')
            
            else:
                print("❌ Invalid choice. Please enter a number between 0-9")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        system = SmartAttendanceSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
