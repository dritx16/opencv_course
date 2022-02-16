# Painting by webcam
import cv2
import numpy as np

# Listing colors by finding their values using color_picker.py
myColors = [[17, 49, 60, 183, 0, 255],
            [90, 140, 74, 255, 109, 255],
            [50, 179, 80, 255, 253, 255]]   # Orange, dark blue, red values by color_picker.by

# Color values to display
myColorsValues = [[51, 153, 255],     # BGR
                  [204, 102, 0],
                  [0, 0, 255]]

# Listing pts to draw on canvas
myPts = []      # [x, y, colorId]


# We need contours to paint.
def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            prm = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * prm, True)
            x, y, w, h = cv2.boundingRect(approx)

    return x + w//2, y

# Finding known colors on webcam
def find_color(img, myColors, myColorsValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPts = []
    for color in myColors:
        lower = np.array(color[0::2])
        upper = np.array(color[1::2])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = get_contours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorsValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPts.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)
    return  newPts


# Drawing on canvas
def draw_on_canvas(myPts, myColorsValues):
    for pt in myPts:
        cv2.circle(imgResult, (pt[0], pt[1]), 10, myColorsValues[pt[2]], cv2.FILLED)


# Getting webcam
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPts = find_color(img, myColors, myColorsValues)
    if len(newPts) != 0:
        for newPt in newPts:
            myPts.append(newPt)

    if len(myPts) != 0:
        draw_on_canvas(myPts, myColorsValues)

    cv2.imshow("Webcam", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
