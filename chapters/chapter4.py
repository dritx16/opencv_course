# Draw shapes on images, and how to put text on images
import cv2
import numpy as np
path = "/home/suleyman/PycharmProjects/pythonProject/resources/"

img = np.zeros((512, 512, 3), np.uint8)
print(img.shape)

# img[:] = 100, 200, 100    # to paint whole or some part of an image

cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 2)
cv2.line(img, (img.shape[0], 0), (0, img.shape[1]), (255, 0, 0), 2)
cv2.rectangle(img, (img.shape[0] // 4, img.shape[1] // 4), (3 * img.shape[0] // 4, 3 * img.shape[1] // 4), (0, 0, 255), 2)      # To fill whole rectangle cv2.FILLED instead of 2
cv2.circle(img, (img.shape[0] // 2, img.shape[1] // 2), 25, (255, 255, 0), 2)
cv2.putText(img, "suleyman learns opencv", (20, 20), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)

cv2.imshow("np image", img)
cv2.waitKey(0)
