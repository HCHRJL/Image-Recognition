#!/usr/bin/env python3.8
# -*- coding: UTF-8 -*-
# Python libs
####################################################################################################################################
import rospy
import numpy as np
import time
import cv2 as cv
import cv2
####################################################################################################################################
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Point
####################################################################################################################################
bar_name = "Hmin      色調", "Smin 飽和度", "Vmin      亮度","Hmax      色調", "Smax 飽和度", "Vmax      亮度","Xmin ", "Ymim", "Xmax", "Ymax"
bar_count = 180, 255, 255, 180, 255, 255, 640, 480, 640, 480
hsv_min = [114, 19, 116]
hsv_max = [145, 102, 187]
border = [0, 0, 640, 480]
bar_init = hsv_min[0], hsv_min[1], hsv_min[2],hsv_max[0], hsv_max[1], hsv_max[2],border[0], border[1], border[2], border[3]
bridge = CvBridge()
kernel = np.ones((5,5),np.uint8)
def track(x):
    global hsv_min, hsv_max, border
    for j in range(10):
        if 0 <= j < 3:
            hsv_min[j] = cv.getTrackbarPos(bar_name[j], "TRACKBAR 軌跡條")
        elif 3 <= j < 6:
            hsv_max[j - 3] = cv.getTrackbarPos(bar_name[j], "TRACKBAR 軌跡條")
        else:
            border[j - 6] = cv.getTrackbarPos(bar_name[j], "TRACKBAR 軌跡條")
cv.namedWindow("TRACKBAR 軌跡條", cv.WINDOW_AUTOSIZE )
cv.resizeWindow("TRACKBAR 軌跡條", 600, 450)
for i in range(10):
    cv.createTrackbar(bar_name[i], "TRACKBAR 軌跡條", 0, bar_count[i], track)
    cv.setTrackbarPos(bar_name[i], "TRACKBAR 軌跡條", bar_init[i])
####################################################################################################################################
KD = 10 #cm
KW = 10.5  #cm
KH = 7.4  #cm
img = cv2.imread('1123.jpg',cv2.IMREAD_COLOR)
####################################################################################################################################
#def distance_to_camera(knownWidth, focalLength, perWidth):
#    return (knownWidth * focalLength) / perWidth
####################################################################################################################################
hsv1 = cv.cvtColor(img, cv.COLOR_BGR2HSV)
gray1 = cv.inRange(hsv1, (hsv_min[0], hsv_min[1], hsv_min[2]), (hsv_max[0], hsv_max[1], hsv_max[2]))
opening1 = cv.morphologyEx(gray1, cv.MORPH_OPEN, kernel)
contour1, _ = cv.findContours(opening1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
####################################################################################################################################
if len(contour1) > 0:
   minarea = 1000
   for c in range(len(contour1)):
       area = cv.contourArea(contour1[c])
       if area > minarea:
          max_idx = np.argmax(np.array(contour1[c]))
          pp = cv2.minAreaRect(contour1[c])
          box1 = cv.boxPoints(pp)
          box1 = np.int0(box1)
          a = round(box1[1][1]*0.025,1)
          b = round(box1[1][0]*0.025,1)
####################################################################################################################################
          F = (pp[1][0] * KD) / KW
          print('焦距（F）= ',round(F,1))
####################################################################################################################################
          text = "w:  "+ str(a) + 'cm' + "  h:  " + str(b) + 'cm'
          cv.drawContours(img, [box1], -1, (0, 255, 0), 5)
          cv.putText(img, text, (10, 30),cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA, 0)
####################################################################################################################################
          cv.imshow("opening", opening1)
          cv.imshow("bgr", img)
####################################################################################################################################
def callback(ros_img):
    bgr = bridge.compressed_imgmsg_to_cv2(ros_img)
    timeEND = 0
    timeST = 0
    timeST = time.time()
    fps = 1/(timeST - timeEND)
    timeEND = timeST
    print( "FPS : {0}".format(fps))
    cv.putText(bgr,"FPS {0}".format(float('%.1f' % fps)),(250, 50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),2)
####################################################################################################################################
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    gray = cv.inRange(hsv, (hsv_min[0], hsv_min[1], hsv_min[2]), (hsv_max[0], hsv_max[1], hsv_max[2]))
    opening = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel)
    contour, _ = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#    pub = rospy.Publisher('chatter', Point, queue_size=1000)
####################################################################################################################################
    if len(contour) > 0:
       minarea = 1000
       for i in range(len(contour)):
           area = cv.contourArea(contour[i])
           if area > minarea:
              max_idx = np.argmax(np.array(area))
              x, y, w, h = cv.boundingRect(contour[i])
              w1 = round(w*0.025,1)
              h1 = round(h*0.025,1)
              rect = cv2.minAreaRect(contour[i])
              box = cv.boxPoints(rect)
              box = np.int0(box)
#              distance_inches = distance_to_camera(KNOWN_WIDTH, focalLength, box[1][1])
              nd = (KW * F)/rect[1][0]
              text = "w:  "+ str(w1) + 'cm' + "  h:  " + str(h1) + 'cm'
              cv.drawContours(bgr, [box], -1, (0, 255, 0), 5)
              cv.putText(bgr, text, (10, 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA, 0)
#              cv.putText(bgr, "%.2fcm" % (distance_inches*2.5), (bgr.shape[1] - 300, bgr.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
              cv.putText(bgr, "%.2fcm" % (nd), (bgr.shape[1] - 300, bgr.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
####################################################################################################################################
    cv.imshow("opening 黑白濾波", opening)
    cv.imshow("bgr 攝影畫面", bgr)
    cv.waitKey(1)
####################################################################################################################################
#def calculate_Distance(image_path, focalLength_value):
#    image = cv2.imread(image_path)
#    marker = find_marker(image)
####################################################################################################################################
def listener():
    rospy.init_node('center')
    rospy.Subscriber("/usb_cam/image_raw/compressed", CompressedImage, callback)
    rospy.spin()

if  __name__ == '__main__':
    listener()
