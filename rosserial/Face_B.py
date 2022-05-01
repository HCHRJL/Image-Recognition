#!/usr/bin/env python3.8
# -*- coding: UTF-8 -*-
###############################################################################
import rospy
import cv2 as cv
import cv2
import numpy as np
###############################################################################
from geometry_msgs.msg import Point,Vector3
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
###############################################################################
face_cascade = cv.CascadeClassifier('X.xml')
#face_cascade = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')
bridge = CvBridge()
###############################################################################
def callback(ros_img):
    bgr = bridge.compressed_imgmsg_to_cv2(ros_img)
    gray = cv.cvtColor(bgr, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.15 ,10 )
###############################################################################
    for (x, y, w, h) in faces:
        X = float((x+w)/2)
        Y = float((y+h)/2)
        Z = float()
        pub = rospy.Publisher("face", Vector3, queue_size=1)
        pub.publish(X,Y,Z)
        print([X,Y,0.0])
        cv.rectangle(bgr, (x, y), (x+w, y+h), (0, 255, 0), 3)
    bgr = cv.flip(bgr,1)
    cv.imshow("bgr 攝影畫面", bgr)
    cv.waitKey(1)
################################################################################
def listener():
    rospy.init_node('center')
    rospy.Publisher("face", Vector3, queue_size=1)
    rate = rospy.Rate(0.1)
    rospy.Subscriber("/usb_cam/image_raw/compressed", CompressedImage, callback)
    rospy.spin()
################################################################################
if  __name__ == '__main__':
    listener()
