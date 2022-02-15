# Resize and crop functions
import cv2
import numpy as np

path = "/home/suleyman/PycharmProjects/pythonProject/resources/"

img = cv2.imread(path + "linkedin_photo.jpeg")
print(img.shape)    # (height, width, #of channels(BGR))

# Resizing an image
imgResize = cv2.resize(img, (400, 400))     # Height comes first in the argument
print(imgResize.shape)

# Cropping an image
imgCropped = img[0:200, 200:500]

cv2.imshow("image", img)
cv2.imshow("resized image", imgResize)
cv2.imshow("cropped image", imgCropped)
cv2.waitKey(0)