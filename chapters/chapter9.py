# Face detection by cv2 cascades
import cv2
import numpy as np
path = "/home/suleyman/PycharmProjects/pythonProject/resources/"


face_cascade = cv2.CascadeClassifier(path + "haarcascade_frontalface_default.xml")
img = cv2.imread(path + "linkedin_photo.jpeg")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

cv2.imshow("Result", img)
cv2.waitKey(0)
