import cv2
import numpy as np
import os
import pickle

class FaceTrainer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.faces_dir = 'faces'
        self.labels = {}
        self.current_id = 0
        self.label_ids = {}
        
    def create_faces_directory(self):
        """Create directory to store face images"""
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
            print(f"Created '{self.faces_dir}' directory")
            print("Please create subdirectories for each person with their face images")
            print("Example: faces/John/image1.jpg, faces/John/image2.jpg")
        else:
            print(f"'{self.faces_dir}' directory already exists")
    
    def collect_face_samples(self, person_name, num_samples=30):
        """Collect face samples from webcam for a person"""
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
        
        person_dir = os.path.join(self.faces_dir, person_name)
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        print(f"Collecting {num_samples} face samples for {person_name}")
        print("Press 's' to capture a sample, 'q' to finish")
        
        sample_count = 0
        
        while sample_count < num_samples:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
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
                    print(f"Saved sample {sample_count + 1}")
                    sample_count += 1
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"Collected {sample_count} samples for {person_name}")
    
    def train_model(self):
        """Train the face recognition model from collected face images"""
        if not os.path.exists(self.faces_dir):
            print(f"'{self.faces_dir}' directory not found. Please create it and add face images.")
            return
        
        print("Training face recognition model...")
        
        face_samples = []
        ids = []
        
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
            print("No face images found in the faces directory")
            return
        
        # Train the recognizer
        self.recognizer.train(face_samples, np.array(ids))
        
        # Save the trained model
        self.recognizer.save('trainer.yml')
        
        # Save the labels
        with open('labels.pickle', 'wb') as f:
            pickle.dump(self.label_ids, f)
        
        print(f"Training completed! Model saved as 'trainer.yml'")
        print(f"Trained on {len(face_samples)} face images")
        print(f"Labels: {self.label_ids}")

if __name__ == "__main__":
    trainer = FaceTrainer()
    
    print("Face Training Module")
    print("1. Create faces directory")
    print("2. Collect face samples from webcam")
    print("3. Train model from existing images")
    
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == '1':
        trainer.create_faces_directory()
    elif choice == '2':
        person_name = input("Enter person's name: ")
        num_samples = input("Enter number of samples to collect (default 30): ")
        num_samples = int(num_samples) if num_samples else 30
        trainer.collect_face_samples(person_name, num_samples)
    elif choice == '3':
        trainer.train_model()
    else:
        print("Invalid choice")
