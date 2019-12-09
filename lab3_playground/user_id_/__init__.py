import cv2 as cv
import numpy as np
import time
import os


class UserID:
    def __init__(self, username, cam_id=0):
        self.user_dir = f"{os.path.join(os.path.dirname(__file__), '')}users/{username}/"
        self.cap = cv.VideoCapture(cam_id)
        self.face_cascade = cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        self.recognizer = cv.face.LBPHFaceRecognizer_create()

    def register(self, password):
        pass

    def log(self):
        pass

    def _detect_grayscale_face(self, img):
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(img_gray, scaleFactor=1.5, minNeighbors=5)

        if len(faces) != 1:
            return None

        x, y, w, h = faces[0]

        return img_gray[y:y+h, x:x+w]


base_dir = os.path.join(os.path.dirname(__file__), '')


def detect_face(color_frame, cascade):
    gray_frame = cv.cvtColor(color_frame, cv.COLOR_BGR2GRAY)
    gray_frame = cv.equalizeHist(gray_frame)

    face = cascade.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=5)

    for x, y, w, h in face:
        roi = gray_frame[y:y+h, x:x+w]
        return roi




def register_user(username, password):
    user_dir = base_dir + 'users/' + username + '/'

    if not os.path.exists(user_dir):
        cap = cv.VideoCapture(0)

        cascade_path = cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        face_cascade = cv.CascadeClassifier(cascade_path)
        recognizer = cv.face.LBPHFaceRecognizer_create()

        x_train = []
        y_labels = []

        while True:
            ret, color_frame = cap.read()

            face_arr = detect_face(color_frame, face_cascade)
            resized_face = cv.resize(face_arr, (140, 140), interpolation=cv.INTER_AREA)
            x_train.append(np.array(resized_face, 'uint8'))
            y_labels.append(0)

            cv.imshow('user id', color_frame)

            if cv.waitKey(20) & 0xFF == ord('q'):
                break

        os.mkdir(user_dir)

        with open(user_dir + 'password.txt', 'w') as f:
            f.write(password)

        recognizer.train(x_train, np.array(y_labels))
        recognizer.save(user_dir + 'training.yml')

        return True

    return False


def log_user(username):
    user_dir = base_dir + 'users/' + username + '/'

    if os.path.exists(user_dir):
        training_path = user_dir + 'training.yml'

        cap = cv.VideoCapture(0)

        cascade_path = cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        face_cascade = cv.CascadeClassifier(cascade_path)

        recognizer = cv.face.LBPHFaceRecognizer_create()
        recognizer.read(training_path)

        while True:
            ret, color_frame = cap.read()

            face = detect_face(color_frame, face_cascade)
            if face is not None:
                resized_face = cv.resize(face, (140, 140), interpolation=cv.INTER_AREA)
                print(recognizer.predict(resized_face))

            cv.imshow('user id', color_frame)

            if cv.waitKey(20) & 0xFF == ord('q'):
                break

    return False


def create_trainer(img_folder):
    img_dir = f'{base_dir}{img_folder}/'

    recognizer = cv.face.LBPHFaceRecognizer_create()
    cascade_path = cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
    face_cascade = cv.CascadeClassifier(cascade_path)

    trainer_array = []
    labels = []

    with os.scandir(img_dir) as folders:
        for folder in folders:
            folder_path = f"{img_dir}{folder.name}/"
            label = int(folder.name)

            with os.scandir(folder_path) as imgs:
                for img in imgs:
                    img_path = f"{folder_path}{img.name}"

                    color_img = cv.imread(img_path)

                    face = detect_face(color_img, face_cascade)

                    if face is not None:
                        dim = (140, 140)
                        resized_face = cv.resize(face, dim, interpolation=cv.INTER_AREA)
                        trainer_array.append(np.array(resized_face, 'uint8'))
                        labels.append(label)

    cap = cv.VideoCapture(0)

    for _ in range(3):
        ret, color_fr = cap.read()

        face = detect_face(color_fr, face_cascade)

        if face is not None:
            dim = (140, 140)
            resized_face = cv.resize(face, dim, interpolation=cv.INTER_AREA)
            trainer_array.append(np.array(resized_face, 'uint8'))
            labels.append(0)

        time.sleep(0.5)


    recognizer.train(trainer_array, np.array(labels))
    recognizer.save(base_dir + 'trainer.yml')

def create_trainer_v2():
    recognizer = cv.face.LBPHFaceRecognizer_create()
    trainer = []
    labels = []

    cap = cv.VideoCapture(0)

    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

    for _ in range(100):
        ret, frame = cap.read()

        face = detect_face(frame, face_cascade)

        if face is not None:
            resized_face = cv.resize(face, (200, 200), interpolation=cv.INTER_AREA)
            cv.imwrite(base_dir + 'face.png', resized_face)
            trainer.append(np.array(resized_face, 'uint8'))
            labels.append(0)

        cv.imshow('user id', frame)

    recognizer.train(trainer, np.array(labels))
    recognizer.save(base_dir + 'training.yml')


def log_v2():
    cap = cv.VideoCapture(0)

    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

    recognizer = cv.face.LBPHFaceRecognizer_create(threshold=30)
    recognizer.read(base_dir + 'training.yml')

    while True:
        ret, frame = cap.read()

        face = detect_face(frame, face_cascade)

        if face is not None:
            resized_face = cv.resize(face, (200, 200), interpolation=cv.INTER_AREA)
            print(recognizer.predict(resized_face))

        cv.imshow('user id', frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break

