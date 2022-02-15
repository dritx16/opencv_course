# Basic functions of cv2
import cv2
import numpy as np

path = "/home/suleyman/PycharmProjects/pythonProject/resources/"

img = cv2.imread(path + "linkedin_photo.jpeg")
kernel = np.ones((5, 5), np.uint8)      # Creating a kernel for dialation function

# cvtColor is used for changing the color of the image.
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# GaussianBlur is used for blurring the image.
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)

# Edge detector
imgCanny = cv2.Canny(img, 200, 200)

# Increase the thickness of edges
imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)

# Decrease the thickness of edges
imgEroded = cv2.erode(imgDialation, kernel, iterations=1)

cv2.imshow("gray image", imgGray)
cv2.imshow("blurred image", imgBlur)
cv2.imshow("canny image", imgCanny)
cv2.imshow("dialation image", imgDialation)
cv2.imshow("eroded image", imgEroded)
cv2.waitKey(0)
