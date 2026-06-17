# image code 31
import cv2

recognizer = cv2.face.LBPHFaceRecognizer_create()

# trained model load
recognizer.read("./models/face_model.yml")

print("Model Loaded")