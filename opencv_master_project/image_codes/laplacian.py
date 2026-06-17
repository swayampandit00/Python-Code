# image code 29
import cv2

img = cv2.imread("./assets/sample.jpg", 0)

lap = cv2.Laplacian(img, cv2.CV_64F)

cv2.imshow("Laplacian", lap)
cv2.waitKey(0)
cv2.destroyAllWindows()