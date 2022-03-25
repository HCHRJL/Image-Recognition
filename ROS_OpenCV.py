#!/usr/bin/env python3.8
# -*- coding: UTF-8 -*-
# Python libs


import rospy
import numpy as np # 數據計算相關函式庫
import cv2 as cv # openCV函式庫

from cv_bridge import CvBridge # 影像發布來自ROS裝置 但影像接受處裡在非ROS裝置進行 需要cv_Bridge改格式
from sensor_msgs.msg import CompressedImage

#################################
########## 數值初始設定 ##########
#################################
bar_name = "Hmin", "Smin", "Vmin", "Hmax", "Smax", "Vmax", "Xmin", "Ymim", "Xmax", "Ymax" # 拉條名
bar_count = 180, 255, 255, 180, 255, 255, 640, 480, 640, 480 # 拉條最大值
hsv_min = [0, 0, 0]
hsv_max = [180, 255, 255]
border = [0, 0, 640, 480] # 邊界值 x, y, x, y
bar_init = hsv_min[0], hsv_min[1], hsv_min[2], hsv_max[0], hsv_max[1], hsv_max[2], \
           border[0], border[1], border[2], border[3] # 拉條設定值   \可將指令內容延至下行
bridge = CvBridge()
kernel = np.ones((5,5),np.uint8) # 5×5矩陣 數值皆為1

def track(x): # 取得拉條位置
    global hsv_min, hsv_max, border
    for j in range(10):
        if 0 <= j < 3:
            hsv_min[j] = cv.getTrackbarPos(bar_name[j], "TRACKBAR")
        elif 3 <= j < 6:
            hsv_max[j - 3] = cv.getTrackbarPos(bar_name[j], "TRACKBAR") # j = 3~5	j-3 = 0~2
        else:
            border[j - 6] = cv.getTrackbarPos(bar_name[j], "TRACKBAR") # j = 6~9	j-6 = 0~3
cv.namedWindow("TRACKBAR", cv.WINDOW_AUTOSIZE)
cv.resizeWindow("TRACKBAR", 500, 420)
for i in range(10):
    cv.createTrackbar(bar_name[i], "TRACKBAR", 0, bar_count[i], track)
    cv.setTrackbarPos(bar_name[i], "TRACKBAR", bar_init[i])


#################################
############## ROS ##############
#################################
def callback(ros_img):
    bgr = bridge.compressed_imgmsg_to_cv2(ros_img) # CompressedImage訊息格式改成cv2格式
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    gray = cv.inRange(hsv, (hsv_min[0], hsv_min[1], hsv_min[2]), (hsv_max[0], hsv_max[1], hsv_max[2]))

    opening = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel) # 濾波
    _, contour, _ = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) # cv3版本會返回img, contours, hierarchy
    if len(contour) > 0:
        maxArea = 100
        for i in range(len(contour)):
            area = cv.contourArea(contour[i])
            if area > maxArea:
                maxArea = area
                center, radius = cv.minEnclosingCircle(contour[i])
                cv.circle(bgr, (int(center[0]), int(center[1])), 1, (255, 0, 0), 2)
                cv.circle(bgr, (int(center[0]), int(center[1])), int(radius), (0, 255, 0), 2)

    cv.imshow("opening", opening)
    cv.imshow("bgr", bgr)
    cv.waitKey(1)

def listener():
    rospy.init_node('center')
    rospy.Subscriber("/usb_cam/image_raw/compressed", CompressedImage, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
