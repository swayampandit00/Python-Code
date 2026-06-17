# image code 9
import cv2
import numpy as np

img = cv2.imread("./assets/sample.jpg")

# matrix for move
matrix = np.float32([[1, 0, 100], [0, 1, 50]])

move = cv2.warpAffine(img, matrix, (500, 500))

cv2.imshow("Translate", move)

cv2.waitKey(0)
cv2.destroyAllWindows()