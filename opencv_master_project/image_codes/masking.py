# image code 25
import cv2
import numpy as np

img = cv2.imread("./assets/sample.jpg")

mask = np.zeros(img.shape[:2], dtype="uint8")

cv2.circle(mask, (200,200), 100, 255, -1)

result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("Mask", result)
cv2.waitKey(0)
cv2.destroyAllWindows()