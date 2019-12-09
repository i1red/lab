import cv2 as cv


class Identifier:
    def __init__(self, user_face):
        cascade_path = cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        self.face_cascade = cv.CascadeClassifier(cascade_path)


    def register_user(self):
        pass


    def identify_user(self):
        res = False

        return res