# image code 19
import cv2

img = cv2.imread("./assets/sample.jpg")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow("HSV", hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()