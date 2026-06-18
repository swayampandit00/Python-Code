# image code 8
import cv2

img = cv2.imread("./assets/sample.jpg")

# 1 = horizontal flip
flip = cv2.flip(img, 1)

cv2.imshow("Flip", flip)

cv2.waitKey(0)
cv2.destroyAllWindows()