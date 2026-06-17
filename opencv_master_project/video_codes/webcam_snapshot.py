# video code 7
import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

# image save
cv2.imwrite("photo.jpg", frame)

print("Photo Saved")

cap.release()