# video code 5
import cv2

cap = cv2.VideoCapture("./assets/sample.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    blur = cv2.GaussianBlur(frame, (15,15), 0)

    cv2.imshow("Blur Video", blur)

    if cv2.waitKey(25) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()