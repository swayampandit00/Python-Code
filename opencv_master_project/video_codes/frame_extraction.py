# video code 13
import cv2

cap = cv2.VideoCapture("./assets/sample.mp4")

count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imwrite(f"./assets/frame_{count}.jpg", frame)

    count += 1

cap.release()

print("Frames Extracted")
