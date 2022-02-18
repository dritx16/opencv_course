# Number plate detection
import cv2
import numpy as np

path = "/home/suleyman/PycharmProjects/open_cv_course/resources/"

n_plate_cascade = cv2.CascadeClassifier(path + "haarcascade_russian_plate_number.xml")
img = cv2.imread(path + "1.jpg")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
number_plates = n_plate_cascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in number_plates:
    area = w*h
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(img, "Number Plate", (x, y-5),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
    imgRoi = img[y:y+h, x:x+w]
    cv2.imshow("Result", img)

cv2.imwrite(path + "plate1.jpg", imgRoi)
cv2.waitKey(0)
