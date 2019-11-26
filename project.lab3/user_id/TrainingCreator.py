import cv2 as cv
import numpy as np
import config


class TrainingCreator:
    def __init__(self):
        self.face_cascade = cv.CascadeClassifier(config.FACE_CASCADE)
        self.training = []
        

