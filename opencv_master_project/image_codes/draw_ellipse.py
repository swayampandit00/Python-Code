# image code 14
import cv2
import numpy as np

img = np.zeros((500,500,3), dtype="uint8")

cv2.ellipse(img, (250,250), (100,50), 0, 0, 360, (0,255,255), 3)

cv2.imshow("Ellipse", img)

cv2.waitKey(0)
cv2.destroyAllWindows()