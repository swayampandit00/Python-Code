import cv2

# image load karo
img = cv2.imread("./assets/sample.jpg")

# image show karo
cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()