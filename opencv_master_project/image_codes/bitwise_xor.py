# image code 23
import cv2
import numpy as np

img1 = np.zeros((300,300), dtype="uint8")
img2 = np.zeros((300,300), dtype="uint8")

cv2.rectangle(img1,(50,50),(250,250),255,-1)
cv2.circle(img2,(150,150),100,255,-1)

result = cv2.bitwise_xor(img1, img2)

cv2.imshow("XOR", result)
cv2.waitKey(0)
cv2.destroyAllWindows()