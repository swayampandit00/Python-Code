# image code 4
import cv2

img = cv2.imread("./assets/sample.jpg")

# width=300 height=300
resize = cv2.resize(img, (300, 300))

cv2.imshow("Resized", resize)

cv2.waitKey(0)
cv2.destroyAllWindows()