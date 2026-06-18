# image code 15
import cv2
import numpy as np

img = np.zeros((500,500,3), dtype="uint8")

points = np.array([[100,100],[400,100],[250,400]])

cv2.polylines(img, [points], True, (255,255,255), 3)

cv2.imshow("Polygon", img)

cv2.waitKey(0)
cv2.destroyAllWindows()