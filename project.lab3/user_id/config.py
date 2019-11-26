from cv2.data import haarcascades
from cv2.face import LBPHFaceRecognizer_create


DEFAULT_CAMERA = 0
FACE_SIZE = (140, 140)
USERS_DIR = '../users/'
HAARCASCADES = haarcascades
CREATE_RECOGNIZER = LBPHFaceRecognizer_create