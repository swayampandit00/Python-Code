# image code 26
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("./assets/sample.jpg", 0)

hist = cv2.calcHist([img], [0], None, [256], [0,256])

plt.plot(hist)
plt.show()