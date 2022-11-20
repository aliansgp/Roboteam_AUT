#!/usr/bin/env python3

import rospy
from snesor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2

# import video
cap = cv2.VideoCapture("test3.mp4")
bridge = CvBridge()

def talker():

    pub = rospy.Publisher('/gate', Image, queue_size=1)
    rospy.init_node('image', anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        ret, frame = cap.read()


        if not ret:
             break
        # filter the frame to detect the gate
        frame1 = cv2.inRange(frame, (57, 40, 145),
                            (132, 114, 205))
    # remove noises
        kernel = np.ones((5, 5), np.uint8)
        frame2 = cv2.morphologyEx(frame1, cv2.MORPH_OPEN, kernel, iterations=3)
        frame3 = cv2.morphologyEx(frame1, cv2.MORPH_CLOSE, kernel, iterations=15)

        blur = cv2.GaussianBlur(frame3, (5, 5), 0)
        ret, thresh_img = cv2.threshold(blur, 91, 255, cv2.THRESH_BINARY)

        # find contours
        contours = cv2.findContours(
            thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        # sort contours
        contours = sorted(contours, key=cv2.contourArea)

        # find the biggest contour
        c = max(contours, key=cv2.contourArea)

        # draw a rectangle to cover the biggest contours area
        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 4)

        # find moment
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    # draw circle at center of contour
        cv2.circle(frame, (cX, cY), 4, (0, 0, 0), 20)
        # publish frame
        msg = bridge.cv2_to_imgmsg(frame, 'bgr8')
        pub.publish(msg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if rospy.is_shutdown():
            cap.release()


if __name__ == '__name__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
