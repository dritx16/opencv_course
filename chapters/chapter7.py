# Color detection
import cv2
import numpy as np
path = "/home/suleyman/PycharmProjects/pythonProject/resources/"

img = cv2.imread(path + "linkedin_photo.jpeg")

cv2.imshow("image", img)
cv2.waitKey(0)
