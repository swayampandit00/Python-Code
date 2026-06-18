# image code 5
import cv2

img = cv2.imread("./assets/sample.jpg")

# new file save karo
cv2.imwrite("new_image.jpg", img)

print("Image Saved")