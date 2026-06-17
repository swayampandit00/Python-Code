# image code 24
import cv2
import numpy as np

img = np.zeros((300,300), dtype="uint8")

cv2.rectangle(img,(50,50),(250,250),255,-1)

result = cv2.bitwise_not(img)

cv2.imshow("NOT", result)
cv2.waitKey(0)
cv2.destroyAllWindows()