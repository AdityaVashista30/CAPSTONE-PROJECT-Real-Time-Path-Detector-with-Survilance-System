# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 14:13:58 2020

@author: aditya
"""

from deep_sort_yolov3.main import yoloTracker
from deep_sort_yolov3.yolo import YOLO

yoloTracker(YOLO(),"D:/Projects/CAPSTONE/SAMPLES/video.mp4",'output3_yolov3S2.mp4')


yoloTracker(YOLO(),"D:/Projects/CAPSTONE/SAMPLES/video1.mp4",'output3_yolov3S.mp4')