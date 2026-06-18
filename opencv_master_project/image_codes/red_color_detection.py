# image code 20
import cv2
import numpy as np

img = cv2.imread("./assets/sample.jpg")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower = np.array([0,120,70])
upper = np.array([10,255,255])

mask = cv2.inRange(hsv, lower, upper)

result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("Red Detect", result)
cv2.waitKey(0)
cv2.destroyAllWindows()