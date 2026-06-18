# image code 2
import cv2

img = cv2.imread("./assets/sample.jpg")

# window me image display
cv2.imshow("Display", img)

# 0 matlab key press ka wait
cv2.waitKey(0)
cv2.destroyAllWindows()