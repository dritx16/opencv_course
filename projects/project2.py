# Document Scanner
import cv2
import numpy as np

# Getting webcam
imgWidth = 640
imgHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, imgWidth)
cap.set(4, imgHeight)


# Helper function for multiple joining features
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


# PreProcessing function for documents
def pre_processing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(img, (5, 5), 1)
    imgCanny = cv2.Canny(img, 200, 200)
    kernel = np.ones((5, 5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDialation, kernel, iterations=1)

    return imgThres


# Getting contours for the document
def get_contours(img):
    biggest = np.array([])
    max_area = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 3000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            prm = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * prm, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 15)
    return biggest


def reorder(myPts):
    myPts = myPts.reshape((4, 2))
    myPtsNew = np.zeros((4, 1, 2), np.int32)
    add = myPts.sum(1)
    # print("add", add)

    myPtsNew[0] = myPts[np.argmin(add)]
    myPtsNew[3] = myPts[np.argmax(add)]
    diff = np.diff(myPts, axis=1)
    myPtsNew[1] = myPts[np.argmin(diff)]
    myPtsNew[2] = myPts[np.argmax(diff)]
    # print("New Pts", myPtsNew)
    return  myPtsNew

# Warp perspection to adjust the document
def get_warp(img, biggest):
    biggest = reorder(biggest)
    # print(biggest.shape)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (imgWidth, imgHeight))

    # imgCropped = imgOutput[20:imgOutput.shape[0] - 20:, imgOutput.shape[1] - 20]
    # imgCropped = cv2.resize(imgCropped, (imgWidth, imgHeight))

    return imgOutput

while True:
    success, img = cap.read()
    img = cv2.resize(img, (imgWidth, imgHeight))
    imgContour = img.copy()

    imgThres = pre_processing(img)
    biggest = get_contours(imgThres)
    if biggest.size != 0:
        imgWarped = get_warp(img, biggest)

        imageArr = ([img, imgContour],
                    [imgThres, imgWarped])
        stackedImg = stackImages(imageArr, 0.6)

        cv2.imshow("Work Flow", stackedImg)
        cv2.imshow("Final Document", imgWarped)
    else:
        imageArr = ([img, imgContour],
                    [img, img])
        stackedImg = stackImages(imageArr, 0.6)

        cv2.imshow("Work Flow", stackedImg)
        cv2.imshow("Final", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
