#!/usr/bin/env python3

import rospy 
from snesor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2

cap = cv2.VideoCapture("test3.mp4")
bridge = CvBridge()
def talker():

    pub = rospy.Publisher('/ros',Image,queue_size=1)
    rospy.init_node('image',anonymous=True)
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        # Our operations on the frame come here
        frame1 = cv2.inRange(frame, (206, 179, 34),
                                (255, 227, 181))
        kernel = np.ones((5, 5), np.uint8)
        frame2 = cv2.morphologyEx(frame1, cv2.MORPH_OPEN, kernel, iterations=2)
        frame3 = cv2.morphologyEx(frame2, cv2.MORPH_CLOSE, kernel, iterations=2)

        blur = cv2.GaussianBlur(frame3, (5, 5), 0)
        ret, thresh_img = cv2.threshold(blur, 91, 255, cv2.THRESH_BINARY)

        contours = cv2.findContours(
            thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        contours = sorted(contours, key=cv2.contourArea)
        # draw contours on frame (original)
        cv2.drawContours(frame, contours, 0, (0, 0, 0), 3)
        M = cv2.moments(contours[0])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX, cY), 4, (0, 0, 0), 10)
        
        #publish frame
        msg = bridge.cv2_to_imgmsg(frame,'bgr8')
        pub.publish(msg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if rospy.is_shutdown():
            cap.release()

if __name__=='__name__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

