# video code 8
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.putText(frame,
                "OpenCV Live",
                (50,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    cv2.imshow("Live Text", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()