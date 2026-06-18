# image code 13
import cv2
import numpy as np

img = np.zeros((500,500,3), dtype="uint8")

cv2.circle(img, (250,250), 100, (255,0,0), 3)

cv2.imshow("Circle", img)

cv2.waitKey(0)
cv2.destroyAllWindows()