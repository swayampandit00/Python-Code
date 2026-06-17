# image code 16
import cv2
import numpy as np

img = np.zeros((500,500,3), dtype="uint8")

cv2.putText(img, "Hello OpenCV", (100,250),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (255,255,255), 2)

cv2.imshow("Text", img)
cv2.waitKey(0)
cv2.destroyAllWindows()