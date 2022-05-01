#!/usr/bin/env python3.8
# -*- coding: UTF-8 -*-
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
###############################################################################
bridge = CvBridge()
###############################################################################
cap = cv.VideoCapture('video.MOV')
###############################################################################
if not cap.isOpened():
    print("can not open video file")
    cv.waitKey(2000)
    cap.release()
    quit(-1)
###############################################################################
rospy.init_node('center')
rospy.Publisher("face", Vector3, queue_size=1)
rate = rospy.Rate(0.1)
###############################################################################
while True:
    ret, frame = cap.read()
    if ret == True:
       bgr = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
       gray = cv.cvtColor(bgr, cv.COLOR_BGR2GRAY)
       faces = face_cascade.detectMultiScale(gray, 1.15 ,10 )
################################################################################
       for (x, y, w, h) in faces:
           X = float((x+w)/2)
           Y = float((y+h)/2)
           Z = float()
           pub = rospy.Publisher("face", Vector3, queue_size=1)
           pub.publish(X,Y,Z)
           print([X,Y,0.0])
           cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
       bgr = cv.flip(bgr,1)
       cv.imshow("攝影畫面", frame)
################################################################################
       if cv2.waitKey(16) & 0xFF == ord("x"):
          break

    else:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
