# video code 11
import cv2

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read("./models/face_model.yml")

print("Realtime recognition model loaded")