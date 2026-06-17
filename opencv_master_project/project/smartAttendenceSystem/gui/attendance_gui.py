import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime
import pickle
import threading
from PIL import Image, ImageTk
import sys

class AttendanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Attendance System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")
        
        # Initialize attendance system
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {}
        self.label_ids = {}
        self.current_id = 0
        self.faces_dir = 'faces'
        self.attendance_file = 'attendance.csv'
        self.camera_active = False
        self.cap = None
        
        self.initialize_system()
        self.create_gui()
    
    def initialize_system(self):
        """Initialize all necessary directories and files"""
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
        
        if not os.path.exists(self.attendance_file):
            df = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Status'])
            df.to_csv(self.attendance_file, index=False)
        
        if os.path.exists('trainer.yml') and os.path.exists('labels.pickle'):
            self.recognizer.read('trainer.yml')
            with open('labels.pickle', 'rb') as f:
                self.labels = pickle.load(f)
            self.labels = {v: k for k, v in self.labels.items()}
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#34495e", height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🎓 Smart Attendance System", 
                              font=("Arial", 24, "bold"), bg="#34495e", fg="white")
        title_label.pack(pady=20)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Buttons
        left_panel = tk.Frame(main_frame, bg="#34495e", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        left_panel.pack_propagate(False)
        
        # Buttons
        buttons = [
            ("📷 Collect Face Samples", self.collect_face_samples),
            ("🔄 Train Model", self.train_model),
            ("📹 Start Attendance", self.start_attendance),
            ("⏹ Stop Attendance", self.stop_attendance),
            ("👥 View Users", self.view_users),
            ("📊 View Attendance", self.view_attendance),
            ("📈 Generate Report", self.generate_report),
            ("📤 Export to Excel", self.export_excel),
            ("🗑 Clear Attendance", self.clear_attendance),
        ]
        
        for text, command in buttons:
            btn = tk.Button(left_panel, text=text, command=command,
                           font=("Arial", 11), bg="#3498db", fg="white",
                           relief=tk.FLAT, padx=20, pady=10, cursor="hand2")
            btn.pack(fill=tk.X, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#2980b9"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#3498db"))
        
        # Right panel - Content
        right_panel = tk.Frame(main_frame, bg="#ecf0f1")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Camera preview
        self.camera_frame = tk.Frame(right_panel, bg="#2c3e50")
        self.camera_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.camera_label = tk.Label(self.camera_frame, text="Camera Preview", 
                                    font=("Arial", 14), bg="#2c3e50", fg="white")
        self.camera_label.pack(pady=10)
        
        self.video_label = tk.Label(self.camera_frame, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             font=("Arial", 10), bg="#34495e", fg="white", anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=10, pady=5)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update()
    
    def collect_face_samples(self):
        """Collect face samples from webcam"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Collect Face Samples")
        dialog.geometry("400x300")
        dialog.configure(bg="#34495e")
        
        tk.Label(dialog, text="Enter Person's Name:", font=("Arial", 12), 
                bg="#34495e", fg="white").pack(pady=10)
        
        name_entry = tk.Entry(dialog, font=("Arial", 12))
        name_entry.pack(pady=5, padx=20)
        
        tk.Label(dialog, text="Number of Samples:", font=("Arial", 12), 
                bg="#34495e", fg="white").pack(pady=10)
        
        samples_entry = tk.Entry(dialog, font=("Arial", 12))
        samples_entry.insert(0, "30")
        samples_entry.pack(pady=5, padx=20)
        
        def start_collection():
            name = name_entry.get().strip()
            num_samples = samples_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter a name")
                return
            
            try:
                num_samples = int(num_samples) if num_samples else 30
            except ValueError:
                messagebox.showerror("Error", "Invalid number of samples")
                return
            
            dialog.destroy()
            self.collect_samples_thread(name, num_samples)
        
        tk.Button(dialog, text="Start Collection", command=start_collection,
                 font=("Arial", 12), bg="#2ecc71", fg="white", 
                 relief=tk.FLAT, padx=20, pady=10).pack(pady=20)
    
    def collect_samples_thread(self, name, num_samples):
        """Collect face samples in a separate thread"""
        def collect():
            person_dir = os.path.join(self.faces_dir, name)
            if not os.path.exists(person_dir):
                os.makedirs(person_dir)
            
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam")
                return
            
            self.update_status(f"Collecting {num_samples} samples for {name}...")
            sample_count = 0
            
            while sample_count < num_samples:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, f"Samples: {sample_count}/{num_samples}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Display in GUI
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = ImageTk.PhotoImage(img)
                self.video_label.config(image=img)
                self.video_label.image = img
                self.root.update()
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == 27:  # q or ESC
                    break
                elif key == ord('s') and len(faces) > 0:
                    for (x, y, w, h) in faces:
                        face_roi = gray[y:y+h, x:x+w]
                        sample_path = os.path.join(person_dir, f"{name}_{sample_count}.jpg")
                        cv2.imwrite(sample_path, face_roi)
                        sample_count += 1
                        break
                
                # Auto-capture every 10 frames if face detected
                if len(faces) > 0 and sample_count % 2 == 0:
                    for (x, y, w, h) in faces:
                        face_roi = gray[y:y+h, x:x+w]
                        sample_path = os.path.join(person_dir, f"{name}_{sample_count}.jpg")
                        cv2.imwrite(sample_path, face_roi)
                        sample_count += 1
                        break
                
                if sample_count >= num_samples:
                    break
            
            cap.release()
            self.update_status(f"Collected {sample_count} samples for {name}")
            messagebox.showinfo("Success", f"Collected {sample_count} samples for {name}")
        
        thread = threading.Thread(target=collect)
        thread.daemon = True
        thread.start()
    
    def train_model(self):
        """Train the face recognition model"""
        self.update_status("Training model...")
        
        def train():
            face_samples = []
            ids = []
            self.label_ids = {}
            self.current_id = 0
            
            for root, dirs, files in os.walk(self.faces_dir):
                for file in files:
                    if file.endswith("jpg") or file.endswith("png"):
                        path = os.path.join(root, file)
                        label = os.path.basename(root)
                        
                        if label not in self.label_ids:
                            self.label_ids[label] = self.current_id
                            self.current_id += 1
                        
                        id_ = self.label_ids[label]
                        
                        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            face_samples.append(img)
                            ids.append(id_)
            
            if len(face_samples) == 0:
                messagebox.showerror("Error", "No face images found")
                self.update_status("Training failed")
                return
            
            self.recognizer.train(face_samples, np.array(ids))
            self.recognizer.save('trainer.yml')
            
            with open('labels.pickle', 'wb') as f:
                pickle.dump(self.label_ids, f)
            
            self.labels = {v: k for k, v in self.label_ids.items()}
            
            self.update_status(f"Model trained with {len(face_samples)} images")
            messagebox.showinfo("Success", f"Model trained successfully!\nUsers: {list(self.label_ids.keys())}")
        
        thread = threading.Thread(target=train)
        thread.daemon = True
        thread.start()
    
    def start_attendance(self):
        """Start the attendance system"""
        if not os.path.exists('trainer.yml'):
            messagebox.showerror("Error", "No trained model found. Please train the model first.")
            return
        
        if self.camera_active:
            messagebox.showwarning("Warning", "Camera is already active")
            return
        
        self.camera_active = True
        self.update_status("Starting attendance system...")
        
        def run_attendance():
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam")
                self.camera_active = False
                return
            
            while self.camera_active:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    
                    id_, confidence = self.recognizer.predict(face_roi)
                    
                    if confidence < 100:
                        name = self.labels.get(id_, "Unknown")
                        confidence = f"{100 - confidence:.0f}%"
                        color = (0, 255, 0)
                        self.mark_attendance(name)
                    else:
                        name = "Unknown"
                        confidence = f"{100 - confidence:.0f}%"
                        color = (0, 0, 255)
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, f"{name} ({confidence})", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = ImageTk.PhotoImage(img)
                self.video_label.config(image=img)
                self.video_label.image = img
                self.root.update()
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            if self.cap:
                self.cap.release()
            self.camera_active = False
            self.update_status("Attendance system stopped")
        
        thread = threading.Thread(target=run_attendance)
        thread.daemon = True
        thread.start()
    
    def stop_attendance(self):
        """Stop the attendance system"""
        self.camera_active = False
        if self.cap:
            self.cap.release()
        self.update_status("Attendance system stopped")
    
    def mark_attendance(self, name):
        """Mark attendance for recognized person"""
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        
        df = pd.read_csv(self.attendance_file)
        today_attendance = df[(df['Name'] == name) & (df['Date'] == date)]
        
        if today_attendance.empty:
            new_entry = pd.DataFrame([[name, date, time, 'Present']], 
                                    columns=['Name', 'Date', 'Time', 'Status'])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(self.attendance_file, index=False)
    
    def view_users(self):
        """View registered users"""
        if os.path.exists('labels.pickle'):
            with open('labels.pickle', 'rb') as f:
                self.label_ids = pickle.load(f)
            
            dialog = tk.Toplevel(self.root)
            dialog.title("Registered Users")
            dialog.geometry("400x300")
            dialog.configure(bg="#34495e")
            
            tk.Label(dialog, text=f"Registered Users ({len(self.label_ids)})", 
                    font=("Arial", 14, "bold"), bg="#34495e", fg="white").pack(pady=10)
            
            text = ScrolledText(dialog, font=("Arial", 11), bg="#ecf0f1", fg="#2c3e50")
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            for name in self.label_ids.keys():
                text.insert(tk.END, f"• {name}\n")
        else:
            messagebox.showinfo("Info", "No users registered yet")
    
    def view_attendance(self):
        """View attendance records"""
        df = pd.read_csv(self.attendance_file)
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Attendance Records")
        dialog.geometry("800x500")
        dialog.configure(bg="#34495e")
        
        tk.Label(dialog, text="Attendance Records", font=("Arial", 14, "bold"), 
                bg="#34495e", fg="white").pack(pady=10)
        
        text = ScrolledText(dialog, font=("Consolas", 10), bg="#ecf0f1", fg="#2c3e50")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, df.to_string(index=False))
    
    def generate_report(self):
        """Generate attendance report"""
        df = pd.read_csv(self.attendance_file)
        
        total_records = len(df)
        unique_persons = df['Name'].nunique()
        
        person_stats = df.groupby('Name').size().reset_index(name='Days Present')
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Attendance Report")
        dialog.geometry("600x400")
        dialog.configure(bg="#34495e")
        
        tk.Label(dialog, text="Attendance Report", font=("Arial", 14, "bold"), 
                bg="#34495e", fg="white").pack(pady=10)
        
        report_text = f"Total Records: {total_records}\n"
        report_text += f"Unique Persons: {unique_persons}\n\n"
        report_text += "Attendance by Person:\n"
        report_text += person_stats.to_string(index=False)
        
        text = ScrolledText(dialog, font=("Arial", 11), bg="#ecf0f1", fg="#2c3e50")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, report_text)
    
    def export_excel(self):
        """Export attendance to Excel"""
        try:
            df = pd.read_csv(self.attendance_file)
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Save attendance report"
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Attendance exported to {file_path}")
        except ImportError:
            messagebox.showerror("Error", "openpyxl not installed. Install with: pip install openpyxl")
    
    def clear_attendance(self):
        """Clear all attendance records"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all attendance records?"):
            df = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Status'])
            df.to_csv(self.attendance_file, index=False)
            messagebox.showinfo("Success", "Attendance records cleared")
    
    def on_closing(self):
        """Handle window closing"""
        self.camera_active = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
