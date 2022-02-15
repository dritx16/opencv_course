# Warp Perspective
import cv2
import numpy as np
path = "/home/suleyman/PycharmProjects/pythonProject/resources/"

img = cv2.imread(path + "linkedin_photo.jpeg")

width, height = 250, 250
pts1 = np.float32([[263, 188], [448, 196], [263, 404], [448, 404]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
imgOutput = cv2.warpPerspective(img, matrix, (width, height))

cv2.imshow("image", img)
cv2.imshow("warped image", imgOutput)
cv2.waitKey(0)
