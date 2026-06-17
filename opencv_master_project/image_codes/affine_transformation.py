# image code 10
import cv2
import numpy as np

img = cv2.imread("./assets/sample.jpg")

pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])

matrix = cv2.getAffineTransform(pts1, pts2)

result = cv2.warpAffine(img, matrix, (300,300))

cv2.imshow("Affine", result)

cv2.waitKey(0)
cv2.destroyAllWindows()