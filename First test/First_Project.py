#Seyed Ali Abdollahian

#This lines run for find HSV range for irange filter:
'''
import cv2

def nothing(x):
    pass

img_original = cv2.imread("p1.png")
img_hsv = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

cv2.namedWindow("colors")

cv2.createTrackbar('LowerbH', "colors", 0, 255,nothing)
cv2.createTrackbar('LowerbS', "colors", 0, 255,nothing)
cv2.createTrackbar('LowerbV', "colors", 0, 255,nothing)
cv2.createTrackbar('UpperbH', "colors", 255, 255,nothing)
cv2.createTrackbar('UpperbS', "colors", 255, 255,nothing)
cv2.createTrackbar('UpperbV', "colors", 255, 255,nothing)

while(1):
    lowerbH = cv2.getTrackbarPos('LowerbH', "colors")
    lowerbS = cv2.getTrackbarPos('LowerbS', "colors")
    lowerbV = cv2.getTrackbarPos('LowerbV', "colors")
    upperbH = cv2.getTrackbarPos('UpperbH', "colors")
    upperbS = cv2.getTrackbarPos('UpperbS', "colors")
    upperbV = cv2.getTrackbarPos('UpperbV', "colors")
    
    img_target = cv2.inRange(img_original, (lowerbH, lowerbS, lowerbV), (upperbH, upperbS, upperbV))
    
    img_specifiedColor = cv2.bitwise_and(img_original, img_original, mask = img_target)
    cv2.imshow("colors", img_specifiedColor)
    #cv2.imshow("colors", img_target)

    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows()
'''


#import libraries
import cv2
import numpy as np

#import image
img_original = cv2.imread("p1.png")

#filter the image with founded range
img_target = cv2.inRange(img_original, (29, 14, 99),
                                       (53, 42, 127))

#use morphology for delete noises
kernel = np.ones((5,5),np.uint8)
img_target = cv2.morphologyEx(img_target,cv2.MORPH_OPEN,kernel,iterations=1)
img_target = cv2.morphologyEx(img_target,cv2.MORPH_CLOSE,kernel,iterations=4)

#find edges to find the contours better
img_target = cv2.Canny(img_target,100,200)

#find contours
contours, hierarchy = cv2.findContours(image=img_target,mode=cv2.RETR_LIST,
                                       method=cv2.CHAIN_APPROX_SIMPLE)

#sort contours with area
contours = sorted(contours, key=cv2.contourArea)

#draw biggest contour on a copy from original image
img_copy = img_original.copy()
cv2.drawContours(image=img_copy,contours=contours,contourIdx=0,
                 color=(0,255,0),thickness=2,lineType=cv2.LINE_AA)

#find center of contour with moment(more info:'en.wikipedia.org/wiki/Image_moment')
M = cv2.moments(contours[0])
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
cv2.circle(img_copy, (cX, cY), 4, (0, 255, 0), -1)

#save the result
cv2.imwrite('img_with_contour.jpg',img_copy)