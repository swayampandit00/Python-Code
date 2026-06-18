import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime
import pickle

class SmartAttendanceSystem:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {}
        self.attendance_file = 'attendance.csv'
        self.load_trained_model()
        
    def load_trained_model(self):
        """Load the trained face recognition model"""
        if os.path.exists('trainer.yml') and os.path.exists('labels.pickle'):
            self.recognizer.read('trainer.yml')
            with open('labels.pickle', 'rb') as f:
                self.labels = pickle.load(f)
            self.labels = {v: k for k, v in self.labels.items()}
            print("Model loaded successfully!")
        else:
            print("No trained model found. Please train the model first using train_faces.py")
    
    def mark_attendance(self, name):
        """Mark attendance for the recognized person"""
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        
        # Create attendance file if it doesn't exist
        if not os.path.exists(self.attendance_file):
            df = pd.DataFrame(columns=['Name', 'Date', 'Time'])
            df.to_csv(self.attendance_file, index=False)
        
        # Read existing attendance
        df = pd.read_csv(self.attendance_file)
        
        # Check if person already marked attendance today
        today_attendance = df[(df['Name'] == name) & (df['Date'] == date)]
        
        if today_attendance.empty:
            # Mark new attendance
            new_entry = pd.DataFrame([[name, date, time]], columns=['Name', 'Date', 'Time'])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(self.attendance_file, index=False)
            print(f"Attendance marked for {name} at {time}")
            return True
        else:
            print(f"{name} already marked attendance today at {today_attendance.iloc[0]['Time']}")
            return False
    
    def run_attendance_system(self):
        """Run the real-time attendance system"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        print("Press 'q' to quit the attendance system")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            
            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                
                # Recognize the face
                if os.path.exists('trainer.yml'):
                    id_, confidence = self.recognizer.predict(face_roi)
                    
                    if confidence < 100:  # Confidence threshold
                        name = self.labels.get(id_, "Unknown")
                        confidence = f"{100 - confidence:.0f}%"
                        
                        # Mark attendance
                        self.mark_attendance(name)
                        
                        color = (0, 255, 0)  # Green for recognized
                    else:
                        name = "Unknown"
                        confidence = f"{100 - confidence:.0f}%"
                        color = (0, 0, 255)  # Red for unknown
                else:
                    name = "No Model"
                    confidence = "N/A"
                    color = (255, 0, 0)  # Blue for no model
                
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

if __name__ == "__main__":
    system = SmartAttendanceSystem()
    system.run_attendance_system()
