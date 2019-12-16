from cv2.data import haarcascades
from cv2.face import LBPHFaceRecognizer_create
import os

DEFAULT_CAMERA = 0
USERS_DIR =  '/'.join(os.path.join(os.path.dirname(__file__), '').split('/')[:-2]) + '/tests/test_users/'
FACE_SIZE = (140, 140)
FACE_CASCADE = haarcascades + 'haarcascade_frontalface_alt2.xml'
CREATE_RECOGNIZER = LBPHFaceRecognizer_create
MAX_DISTANCE = 65

