# image code 11
import cv2
import numpy as np

img = np.zeros((500,500,3), dtype="uint8")

# line draw
cv2.line(img, (50,50), (400,400), (255,255,255), 3)

cv2.imshow("Line", img)

cv2.waitKey(0)
cv2.destroyAllWindows()