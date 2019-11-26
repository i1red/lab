import cv2 as cv
import numpy as np
import config


class TrainingCreator:
    def __init__(self):
        self.face_cascade = cv.CascadeClassifier(config.FACE_CASCADE)
        self.training = []

    def add_item(self, item: '2d array'):
        if item.shape == config.FACE_SIZE:
            self.training.append(item)
        else:
            raise BaseException

    def detect_face(self, img):
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray_img = cv.equalizeHist(gray_img)

        faces = self.face_cascade.detectMultiScale(gray_img, scaleFactor=1.5, minNeighbors=5)
        if len(faces) != 1:
            return False

        x, y, w, h = faces[0]
        face_roi = gray_img[y:y+h, x:x+w]
        face_roi = cv.resize(face_roi, config.FACE_SIZE, interpolation=cv.INTER_AREA)
        self.training.append(np.array(face_roi, 'uint8'))

        return True