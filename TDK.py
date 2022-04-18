#!/usr/bin/env python3.8
# -*- coding: UTF-8 -*-
#######################################################################################################################
import rospy
import cv2 as cv
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
#cap = cv.VideoCapture('TDK.mp4')
#cap = cv.VideoCapture('113.mp4')
cap = cv.VideoCapture(0)
from cv_bridge import CvBridge
from geometry_msgs.msg import Point
#######################################################################################################################
cv.namedWindow("video 影片", cv.WINDOW_NORMAL)
cv.namedWindow("video 座標", cv.WINDOW_NORMAL)
cv.namedWindow("video 路線", cv.WINDOW_NORMAL)
cv.namedWindow("video 角點", cv.WINDOW_NORMAL)
cv.namedWindow("opening 黑白濾波 紅色", cv.WINDOW_NORMAL)
cv.namedWindow("opening 黑白濾波 綠色", cv.WINDOW_NORMAL)
cv.namedWindow("opening 黑白濾波 藍色", cv.WINDOW_NORMAL)
cv.namedWindow("opening 黑白濾波 黑色", cv.WINDOW_NORMAL)
cv.moveWindow("video 影片", 60, 25)
cv.moveWindow("video 座標", 715, 25)
cv.moveWindow("video 路線", 715, 450)
cv.moveWindow("video 角點", 1400, 25)
cv.moveWindow("opening 黑白濾波 紅色", 60, 450)
cv.moveWindow("opening 黑白濾波 綠色", 400 , 450)
cv.moveWindow("opening 黑白濾波 藍色", 60, 700)
cv.moveWindow("opening 黑白濾波 黑色", 400, 700)
cv.resizeWindow("video 影片", 640, 360)
cv.resizeWindow("video 座標", 600, 360)
cv.resizeWindow("video 路線", 320, 200)
cv.resizeWindow("video 角點", 600, 360)
cv.resizeWindow("opening 黑白濾波 紅色", 320,200)
cv.resizeWindow("opening 黑白濾波 綠色", 320,200)
cv.resizeWindow("opening 黑白濾波 藍色", 320,200)
cv.resizeWindow("opening 黑白濾波 黑色", 320,200)
#######################################################################################################################
while True:
    ret, frame = cap.read()
    ret, frame2 = cap.read()
    ret, frame3 = cap.read()
    ret, frame4 = cap.read()
    if ret == True:
#######################################################################################################################
        bridge = CvBridge()
#######################################################################################################################
        kernel = np.ones((5,5),np.uint8)
        erosion = cv2.erode(frame, kernel, 2)
        dilate = cv2.dilate(erosion, kernel, iterations = 2)
#######################################################################################################################
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#######################################################################################################################
#        lower_red = np.array([169, 0, 230])
#        upper_red = np.array([180, 255, 255])

        lower_red = np.array([0, 36 ,200])
        upper_red = np.array([180, 255, 255])

        lower_green = np.array([35, 43, 124])
        upper_green = np.array([77, 255, 255])

#        lower_green = np.array([35, 43, 124])
#        upper_green = np.array([77, 255, 255])

        lower_blue = np.array([100, 43, 46])
        upper_blue = np.array([124, 255, 255])

        lower_black = np.array([0, 0, 0])
        upper_black = np.array([0, 0, 0])
#######################################################################################################################
        red_mask = cv2.inRange(hsv, lower_red, upper_red)

        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        black_mask = cv2.inRange(hsv, lower_black, upper_black)
#######################################################################################################################
#        The_mask1 = cv2.bitwise_or(red_mask, green_mask)
#        The_mask2 = cv2.bitwise_or(The_mask1, black_mask)
#        gray0 = cv.inRange(hsv, (hsv_redmin[0], hsv_redmin[1], hsv_redmin[2]), (hsv_redmax[0], hsv_redmax[1], hsv_redmax[2]))
#        gray1 = cv.inRange(hsv, (hsv_blkmin[0], hsv_blkmin[1], hsv_blkmin[2]), (hsv_blkmax[0], hsv_blkmax[1], hsv_blkmax[2]))
#        The_gray = cv2.bitwise_or(gray0, gray1)
#######################################################################################################################
        opening1 = cv.morphologyEx(red_mask, cv.MORPH_OPEN, kernel)
        opening2 = cv.morphologyEx(green_mask, cv.MORPH_OPEN, kernel)
        opening3 = cv.morphologyEx(blue_mask, cv.MORPH_OPEN, kernel)
        opening4 = cv.morphologyEx(black_mask, cv.MORPH_OPEN, kernel)
#######################################################################################################################
        contour1, _ = cv.findContours(opening1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour2, _ = cv.findContours(opening2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour3, _ = cv.findContours(opening3, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour4, _ = cv.findContours(opening4, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#######################################################################################################################
        edges1 = cv.Canny(red_mask, 50, 150, apertureSize=3)
        edges2 = cv.Canny(green_mask, 50, 150, apertureSize=3)
        edges3 = cv.Canny(blue_mask, 50, 150, apertureSize=3)
        edges4 = cv.Canny(black_mask, 50, 150, apertureSize=3)
#######################################################################################################################
        lines = cv.HoughLinesP(edges1, 2, np.pi/180, 100, minLineLength = 5, maxLineGap = 5 )
        lines2 = cv.HoughLinesP(edges2, 2, np.pi/180, 100, minLineLength = 5, maxLineGap = 5 )
        lines3 = cv.HoughLinesP(edges3, 2, np.pi/180, 100, minLineLength = 5, maxLineGap = 5 )
        lines4 = cv.HoughLinesP(edges4, 2, np.pi/180, 100, minLineLength = 5, maxLineGap = 5 )
#######################################################################################################################
        circles =  cv.HoughCircles(edges4, cv.HOUGH_GRADIENT, 1, 500, param1=50, param2=30, minRadius=0, maxRadius=0)
#######################################################################################################################
#        fast = cv.FastFeatureDetector_create(threshold = 50000,nonmaxSuppression = True)
#        kp = fast.detect(black_mask, None)
#        frame4 = cv.drawKeypoints(frame, kp,None, color=(0,255,0))

        corners = cv2.goodFeaturesToTrack(black_mask, 4, 0.01, 0, None, None, 20, False, False)
#        corners = np.int0(corners)
#######################################################################################################################
        if len(contour1) > 0:
            minarea = 1000
            for i in range(len(contour1)):
                area = cv.contourArea(contour1[i])
                if area > minarea:
                   max_idx = np.argmax(np.array(area))
                   center1, radius = cv.minEnclosingCircle(contour1[i])
                   x = int(center1[0])
                   y = int(center1[1])
                   text = 'x:  '+str(x)+' y:  '+str(y)
                   if lines is not None:
                      for line in lines:
                          x1, y1, x2, y2 = line[0] #lines1.reshape(4)
                          cv.line(frame2, (x1, y1),(x2, y2), (0, 0, 255), 5)
            cv2.drawContours(frame, contour1, -1,(0, 255, 0), 3)
            cv2.drawContours(frame3, contour1, -1,(255, 255, 0), -1)
            cv.circle(frame, (int(center1[0]), int(center1[1])), int(radius), (255, 0, 0), 5)
            cv.circle(frame2, (int(center1[0]), int(center1[1])), 2, (255, 0, 0), 15)
            cv.putText(frame2, text, (10, 120), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3, cv.LINE_AA, 0)
#######################################################################################################################
        if len(contour2) > 0:
           minarea = 1000
           for i in range(len(contour2)):
               area = cv.contourArea(contour2[i])
               if area > minarea:
                  max_idx = np.argmax(np.array(area))
                  center2, radius = cv.minEnclosingCircle(contour2[i])
                  x = int(center2[0])
                  y = int(center2[1])
                  text = 'x:  '+str(x)+' y:  '+str(y)
                  if lines2 is not None:
                     for line in lines2:
                         x1, y1, x2, y2 = line[0] #lines1.reshape(4)
                         cv.line(frame2, (x1, y1),(x2, y2), (0, 0, 255), 5)
           cv2.drawContours(frame, contour2, -1,(0, 255, 0), 3)
           cv2.drawContours(frame3, contour2, -1,(255, 255, 0), -1)
#           cv.circle(frame, (int(center2[0]), int(center2[1])), int(radius), (255, 0, 0), 5)
           cv.circle(frame, (x, y), int(radius), (255, 0, 0), 5)
           cv.circle(frame2, (x, y), 2, (255, 0, 0), 15)
#           cv.circle(frame2, (int(center2[0]), int(center2[1])), 2, (255, 0, 0), 15)
           cv.putText(frame2, text, (10, 120), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3, cv.LINE_AA, 0)
#######################################################################################################################
        if len(contour3) > 0:
            minarea = 1000
            for i in range(len(contour3)):
                area = cv.contourArea(contour3[i])
                if area > minarea:
                   max_idx = np.argmax(np.array(area))
                   center3, radius = cv.minEnclosingCircle(contour3[i])
                   x = int(center3[0])
                   y = int(center3[1])
                   text = 'x:  '+str(x)+' y:  '+str(y)
                   cv.circle(frame, (int(center3[0]), int(center3[1])), int(radius), (255, 0, 0), 5)
                   cv.circle(frame2, (int(center3[0]), int(center3[1])), 2, (255, 0, 0), 15)
                   if lines3 is not None:
                      for line in lines3:
                          x1, y1, x2, y2 = line[0] #lines1.reshape(4)
                          cv.line(frame2, (x1, y1),(x2, y2), (0, 0, 255), 5)
            cv2.drawContours(frame, contour3, -1,(0, 255, 0), 3)
            cv2.drawContours(frame3, contour3, -1,(255, 255, 0), -1)
#            cv.circle(frame, (int(center3[0]), int(center3[1])), int(radius), (255, 0, 0), 5)
#            cv.circle(frame2, (int(center3[0]), int(center3[1])), 2, (255, 0, 0), 15)
#######################################################################################################################
        if len(contour4) > 0:
            minarea = 1000
            for i in range(len(contour4)):
                area = cv.contourArea(contour4[i])
                if area > minarea:
                   max_idx = np.argmax(np.array(area))
                   center4, radius = cv.minEnclosingCircle(contour4[i])
                   x = int(center4[0])
                   y = int(center4[1])
                   text = 'x:  '+str(x)+' y:  '+str(y)
                   rect = cv2.minAreaRect(contour4[i])
#                   box = cv.boxPoints(rect)
#                   box = np.int0(box)

                   for c in range(len(contour4)):
                       x, y, w, h = cv.boundingRect(contour4[c])
                       m = max(w, h)

                       if m < 30:
                          continue

                       vx, vy, x0, y0 = cv.fitLine(contour4[i], cv.DIST_L1, 0, 1e-2, 1e-2)
                       a = vy/vx
                       b = y0 - a * x0
                       maxx = 0
                       maxy = 0
                       minx = 0
                       miny = 10000




#                       for h in range(len(contour4)):
#                           rrt = cv.fitEllipse(contour4[i])
#                           cv.ellipse(frame4, rrt, (0, 0, 255), 2, cv.LINE_AA)
#                           x, y = rrt[0]
#                           cv.circle(frame4, (np.int(x), np.int(y)), 4, (255, 0, 0), -1, 8, 0)


                       for v in contour4[i]:
                           px, py = v[0]
                           rx, ry = v[0]

                    #       x = [maxx,minx,px]
                     #      y = [maxy,miny,py]
                      #     p = np.poly1d(np.polyfit(x,y,2)


                           if maxy < py:
                              maxy = py
                           if miny > py:
                              miny = py
                      # if maxx == minx or maxy == miny :
                       #   minx = maxx + 100

                         #  if maxx < ry:
                         #     maxx = ry
                         #  if minx > ry:
                         #     minx = ry



                           maxx = (maxy - b) / a
                           minx = (miny - b) / a


#                           k = (py-miny)/(px-minx)

#                           if minx > maxx : # and k < 0 : # and  k > -10 :
#                              text1 = 'left'
#                              cv.putText(frame4, text1, (10, 120), cv.FONT_HERSHEY_COMPLEX, 5, (0, 255, 0), 2, cv.LINE_AA, 0)
#
#                           if maxx < minx and k > 0 and k < 100:
#                              text2 = 'right'
#                              cv.putText(frame4, text2, (10, 120), cv.FONT_HERSHEY_COMPLEX, 5, (0, 255, 0), 2 ,cv.LINE_AA, 0)

#                           if maxx == minx and k > 10 or k < -10:
#                              text3 = 'ST'
#                              cv.putText(frame4, text3, (10, 120), cv.FONT_HERSHEY_COMPLEX, 5, (0, 255, 0), 2, cv.LINE_AA, 0)#

#                           if maxy == miny and k == 0 and k > -0.1 and k < 0.1 :
#                              text4 = 'HL'
#                              cv.putText(frame4, text4, (10, 120), cv.FONT_HERSHEY_COMPLEX, 5, (0, 255, 0), 2, cv.LINE_AA, 0)

#                           x = np.array([px,50])
#                           y = np.array([py,50])
#                           poly = np.poly1d(np.polyfit(px, py, 1))

#                           for t in range(30, 250, 1):
#                               y_ = np.int(poly(t))
#                               cv.circle(frame4, (t, y_), 4, (0, 0, 255),20)

#                       if a > 0 :
#                       if a > 0 :
#                       if a < 0 :
#                       if minx < 0 :
#                          minx = 1
#                       if miny < 0 :
#                          miny = 1
#                       if maxx < 0 :
#                          maxx = 1
#                       if maxy < 0 :
#                          maxy = 1
                    #   try:

                       #cv.circle(frame4, (t, y_), 1, (0, 0, 255), 1, 8, 0)

           #            cv.line(frame4, (int(maxx), int(maxy)), (int(minx), int(miny)), (255, 0, 255), 10)
                       cv.line(frame4, (px, py), (px , py), (255, 0, 255), 10)

#                        cv.line(frame4, (px, py), ((int(minx), int(miny)), (255, 0, 255), 40)
#                       cv.line(frame4, (px, py), (rx, ry), (255, 0, 255), 40)

                       cv.circle(frame4,(px,py),10,(255,0,255),30)

#                       cv.circle(frame4,(int(maxx),int(maxy)),4,(255,0,255),40)
#                       cv.circle(frame4,(int(minx),int(miny)),4,(0,255,255),20)
                    #   except OverflowError:
                    #    cv.line(frame4, (0,0), (1,0), (0,0,0),1)
#                       cv.line(frame4, (np.int32(maxx), np.int32(maxy)), (np.int32(minx),np.int32(miny)), (255, 0, 255), 12,8,0)
                       if lines4 is not None:
                          for j in range(lines4.shape[0]):
                              for x1, y1, x2, y2 in lines4[j]:
                                  center_x = int((x1+x2)/2)
                                  center_y = int((y1+y2)/2)
                                  cv.line(frame2, (x1, y1),(x2, y2), (0, 0, 255), 5)


#                              for line in lines4
#                                  if lines is not None:
#                                     x1, y1, x2, y2 = line[0]
#                                     mid = int((x1 + x2) / 2), int((y1 + y2) / 2)
#                                     cv.line(frame2,(300, 240 ),(mid[0] ,mid[1] ), (0, 255, 255), 5)

                                  for l in corners:
                                      x6,y6 = l[0]
                                      cv.circle(frame4,(x6,y6),4,(255,255,0),10)

#                                  if circles is not None:
#                                     for circle in circles[0,:]:
#                                         cv.circle(frame2,(circle[0],circle[1]),circle[2],(0,255,0),5)
#                                         cv.circle(frame2,(circle[0],circle[1]),2,(0,255,0),5)

#            cv.drawContours(frame4, [box], -1, (0, 255, 0), 5)
            cv2.drawContours(frame, contour4, -1,(0, 255, 0), 3)
            cv2.drawContours(frame3, contour4, -1,(255, 255, 0), -1)
            cv.circle(frame, (int(center4[0]), int(center4[1])), int(radius), (255, 0, 0), 5)
            cv.circle(frame2, (int(center4[0]), int(center4[1])), 2, (255, 0, 0), 15)
#            cv.putText(frame4, text, (10, 120), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3, cv.LINE_AA, 0)
#######################################################################################################################
#                          for line in lines:
#                              if lines is not None:
#                                 x1, y1, x2, y2 = line[0]
#                                 mid = int((x1 + x2) / 2), int((y1 + y2) / 2)
#                                 cv.line(frame2,(320, 240 ),(mid[0] ,mid[1] ), (0, 0, 255), 5)
#######################################################################################################################
        cv.imshow("video 影片", frame)
        cv.imshow("video 座標", frame2)
        cv.imshow("video 路線", frame3)
        cv.imshow("video 角點",frame4)
        cv.imshow("opening 黑白濾波 紅色", opening1)
        cv.imshow("opening 黑白濾波 綠色", opening2)
        cv.imshow("opening 黑白濾波 藍色", opening3)
        cv.imshow("opening 黑白濾波 黑色", opening4)
#######################################################################################################################
        if cv.waitKey(50) & 0xFF == ord('q'):
           cap.release()
           cv.destroyAllWindows()
           quit(0)
    else:
           cap.set(cv.CAP_PROP_POS_FRAMES, 0)
