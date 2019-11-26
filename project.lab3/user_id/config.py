from cv2.data import haarcascades
from cv2.face import LBPHFaceRecognizer_create


DEFAULT_CAMERA = 0
FACE_SIZE = (140, 140)
USERS_DIR = '/home/ivan/PycharmProjects/oop-3rd-sem/project.lab3/users/'
FACE_CASCADE = haarcascades + 'haarcascade_frontalface_alt2.xml'
CREATE_RECOGNIZER = LBPHFaceRecognizer_create
MAX_DISTANCE = 45