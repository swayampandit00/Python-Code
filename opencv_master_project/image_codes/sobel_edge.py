# image code 28
import cv2

img = cv2.imread("./assets/sample.jpg", 0)

sobel = cv2.Sobel(img, cv2.CV_64F, 1, 0)

cv2.imshow("Sobel", sobel)
cv2.waitKey(0)
cv2.destroyAllWindows()