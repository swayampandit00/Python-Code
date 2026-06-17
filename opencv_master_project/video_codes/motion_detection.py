# video code 14
import cv2

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while True:
    diff = cv2.absdiff(frame1, frame2)

    cv2.imshow("Motion", diff)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()