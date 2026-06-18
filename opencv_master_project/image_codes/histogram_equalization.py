# image code 27
import cv2

img = cv2.imread("./assets/sample.jpg", 0)

equalized = cv2.equalizeHist(img)

cv2.imshow("Original", img)
cv2.imshow("Equalized", equalized)

cv2.waitKey(0)
cv2.destroyAllWindows()