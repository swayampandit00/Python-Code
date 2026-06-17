# image code 7
import cv2

img = cv2.imread("./assets/sample.jpg")

# rotate clockwise
rotate = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

cv2.imshow("Rotate", rotate)

cv2.waitKey(0)
cv2.destroyAllWindows()