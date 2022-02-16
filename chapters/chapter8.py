# Contour and Shape Detection
import cv2
import numpy as np


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

# Helper function to get contours and shape detection
def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print("Area for the shape: ", area)
        if area > 100:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            prm = cv2.arcLength(cnt, True)
            # print("Arc Length the shape: ", prm)
            approx = cv2.approxPolyDP(cnt, 0.02 * prm, True)
            print("Approx Values: ", len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor == 3: objType = "Tri"
            elif objCor == 4:
                asp_ratio = w/float(h)
                if asp_ratio > 0.95 and asp_ratio < 1.05: objType = "Square"
                else: objType = "Rect"
            elif objCor == 5: objType = "Penta"
            elif objCor == 6: objType = "Hexa"
            elif objCor > 6: objType = "Circle"
            else: objType = "None"

            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(imgContour, objType,
                        (x + (w//2) - 10, y + (h//2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 0, 0), 2)


path = "/home/suleyman/PycharmProjects/pythonProject/resources/"

img = cv2.imread(path + "shapes.png")
imgContour = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)
get_contours(imgCanny)

imgStack = stackImages([[img, imgBlur],
                        [imgContour, imgCanny]], 0.5)

# cv2.imshow("original", img)
# cv2.imshow("gray image", imgGray)
# cv2.imshow("blur image", imgBlur)
cv2.imshow("images", imgStack)
cv2.waitKey(0)
