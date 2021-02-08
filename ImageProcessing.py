# This Python file uses the following encoding: utf-8
import cv2
import numpy as np
import tensorflow as tf
from yolov3.yolov4 import Create_Yolo
from yolov3.utils import detect_image,detect_image_path
from yolov3.configs import *

# use the yolov3 trained model to get image processed
class ImageProcessing:
    def __init__(self):
        #load model :
        self.yolo = Create_Yolo(input_size=YOLO_INPUT_SIZE, CLASSES=TRAIN_CLASSES)
        self.yolo.load_weights("./checkpoints/yolov3_custom") # use keras weights

    # use to get predicted image from path
    def predict_path(self,image_path):
        image=detect_image_path(self.yolo, image_path, "", input_size=YOLO_INPUT_SIZE, show=False, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    # use to get predicted image from image (use by ashcam/video processing)
    def predict_im(self,image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        im=detect_image(self.yolo, image, "", input_size=YOLO_INPUT_SIZE, show=False, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        return im
