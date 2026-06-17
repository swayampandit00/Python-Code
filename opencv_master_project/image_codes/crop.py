# image code 6
import cv2

img = cv2.imread("./assets/sample.jpg")

# y1:y2 , x1:x2
crop = img[50:300, 100:400]

cv2.imshow("Crop", crop)

cv2.waitKey(0)
cv2.destroyAllWindows()