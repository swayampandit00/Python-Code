# video code 2
import cv2

# webcam start
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()