# video code 15
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = (100,150,0)
    upper = (140,255,255)

    mask = cv2.inRange(hsv, lower, upper)

    cv2.imshow("Tracking", mask)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()