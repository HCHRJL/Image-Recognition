#!/usr/bin/env python3.8
# -*- coding: UTF-8 -*-
#######################################################################################################################
import rospy
import cv2 as cv
import cv2
import numpy as np
cap = cv.VideoCapture(0)
from cv_bridge import CvBridge
from geometry_msgs.msg import Point
#######################################################################################################################
bar_name = "Hmin      色調", "Smin 飽和度", "Vmin      亮度", "Hmax      色調", "Smax 飽和度", "Vmax      亮度"
bar_count = 180, 255, 255, 180, 255, 255
hsv_min = [0, 0, 0]
hsv_max = [0, 0, 0]
bar_init = hsv_min[0], hsv_min[1], hsv_min[2], hsv_max[0], hsv_max[1], hsv_max[2]
bridge = CvBridge()
kernel = np.ones((5,5),np.uint8)
#######################################################################################################################
def track(x):
    global hsv_min, hsv_max, border
    for j in range(6):
        if 0 <= j < 3:
            hsv_min[j] = cv.getTrackbarPos(bar_name[j], "TRACKBAR 軌跡條")
        elif 3 <= j < 6:
            hsv_max[j - 3] = cv.getTrackbarPos(bar_name[j], "TRACKBAR 軌跡條")
#######################################################################################################################
cv.namedWindow("TRACKBAR 軌跡條", cv.WINDOW_AUTOSIZE )
cv.namedWindow("video 影片", cv.WINDOW_NORMAL)
cv.namedWindow("video 座標", cv.WINDOW_NORMAL)
cv.namedWindow("video 路線", cv.WINDOW_NORMAL)
cv.namedWindow("opening 黑白濾波", cv.WINDOW_NORMAL)
cv.moveWindow("TRACKBAR 軌跡條", 720, 25)
cv.moveWindow("video 影片", 60, 25)
cv.moveWindow("video 座標", 1150, 25)
cv.moveWindow("video 路線", 1150, 450)
cv.moveWindow("opening 黑白濾波", 60, 450)
cv.resizeWindow("TRACKBAR 軌跡條", 400, 300)
cv.resizeWindow("video 影片", 640, 360)
cv.resizeWindow("video 座標", 640, 360)
cv.resizeWindow("video 路線", 640, 360)
cv.resizeWindow("opening 黑白濾波", 640,360)
#######################################################################################################################
for i in range(6):
    cv.createTrackbar(bar_name[i], "TRACKBAR 軌跡條", 0, bar_count[i], track)
    cv.setTrackbarPos(bar_name[i], "TRACKBAR 軌跡條", bar_init[i])
#######################################################################################################################
while True:
    ret, frame = cap.read()
    ret, frame2 = cap.read()
    ret, frame3 = cap.read()
    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        gray = cv.inRange(hsv, (hsv_min[0], hsv_min[1], hsv_min[2]), (hsv_max[0], hsv_max[1], hsv_max[2]))
        opening = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel)
######################################################################################################################
        contour, _ = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        edges = cv.Canny(gray, 50, 150, apertureSize=3)
        lines = cv.HoughLinesP(edges, 2, np.pi/180, 100, minLineLength = 5, maxLineGap = 5 )
#######################################################################################################################
        if len(contour) > 0:
            minarea = 1000
            for i in range(len(contour)):
                area = cv.contourArea(contour[i])
                if area > minarea:
                   max_idx = np.argmax(np.array(area))
                   center, radius = cv.minEnclosingCircle(contour[i])
                   x = int(center[0])
                   y = int(center[1])
                   text = 'x:  '+str(x)+' y:  '+str(y)
#######################################################################################################################
                   for line in lines:
                       if lines is not None:
                          x1, y1, x2, y2 = line[0]   #line.reshape(4)
                          cv.line(frame2, (x1, y1),(x2, y2), (0, 0, 255), 5)
            cv2.drawContours(frame, contour, -1,(0, 255, 0), 3)
            cv2.drawContours(frame3, contour, -1,(255, 255, 0), -1)
            cv.circle(frame, (int(center[0]), int(center[1])), 2, (0, 0, 255), 8)
            cv.circle(frame, (int(center[0]), int(center[1])), int(radius), (255, 0, 0), 5)
            cv.circle(frame2, (int(center[0]), int(center[1])), 2, (255, 0, 0), 15)
            cv.putText(frame2, text, (10, 120), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3, cv.LINE_AA, 0)
#######################################################################################################################
        cv.imshow("video 影片", frame)
        cv.imshow("video 座標", frame2)
        cv.imshow("video 路線", frame3)
        cv.imshow("opening 黑白濾波", opening)
#######################################################################################################################
        if cv.waitKey(100) & 0xFF == ord('q'):
           cap.release()
           cv.destroyAllWindows()
           quit(0)
    else:
           cap.set(cv.CAP_PROP_POS_FRAMES, 0)
