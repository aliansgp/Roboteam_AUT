import numpy as np
import cv2


cap = cv2.VideoCapture("test3.mp4")
cv2.namedWindow('frame', 0)
cv2.resizeWindow('frame', 300, 300)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)
result = cv2.VideoWriter('rod.mp4',
                         cv2.VideoWriter_fourcc(*'MP4V'),
                         10, size)
while (True):
  # Capture frame-by-frame
   ret, frame = cap.read()

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
   #draw contours on frame (original)
   cv2.drawContours(frame, contours, 0, (0, 0, 0), 3)
   M = cv2.moments(contours[0])
   cX = int(M["m10"] / M["m00"])
   cY = int(M["m01"] / M["m00"])
   cv2.circle(frame, (cX, cY), 4, (0, 0, 0), 10)
   # add frame to result video
   result.write(frame)
   # Display the resulting frame
   cv2.imshow('frame', frame)
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

# When everything done, release the capture & result
cap.release()
result.release()
cv2.destroyAllWindows()
