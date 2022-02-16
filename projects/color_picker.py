# Helper color picker for webcam for project1
import cv2
import numpy as np

# Helper for stacking images
def stackImages(imgArray,scale,lables=[]):
    sizeW = imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver


# Trackbars
def empty(a):
    pass

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)
cv2.createTrackbar("Hue Min.", "Trackbars", 0, 179, empty)
cv2.createTrackbar("Hue Max.", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat Min.", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Sat Max.", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Val Min.", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val Max.", "Trackbars", 255, 255, empty)

# Getting webcam
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
    success, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min.", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max.", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min.", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max.", "Trackbars")
    v_min = cv2.getTrackbarPos("Val Min.", "Trackbars")
    v_max = cv2.getTrackbarPos("Val Max.", "Trackbars")
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    imgStack = stackImages([[img, mask]], 0.5)
    cv2.imshow("Stacked image", imgStack)

    cv2.waitKey(1)
