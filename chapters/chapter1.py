import cv2
print("Package imported")

path = "/resources/"

# Image importing and showing
"""
img = cv2.imread(path + "linkedin_photo.jpeg")
cv2.imshow("output", img)
"""

# Video importing and showing
"""
cap = cv2.VideoCapture(path + "Venice_10.mp4")
while True:
    success, img = cap.read()
    cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
"""

# Webcam importing and showing
cap = cv2.VideoCapture(0)
cap.set(3, 640)     # id = 3 means width
cap.set(4, 480)     # id = 4 means height
cap.set(10, 100)    # id = 10 means brightness
while True:
    success, img = cap.read()
    cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)

