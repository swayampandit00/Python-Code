# video code 12
import cv2

cap = cv2.VideoCapture("./assets/sample.mp4")

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print("Width =", width)
print("Height =", height)

cap.release()