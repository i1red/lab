import cv2 as cv
import time
import config


CASCADE_CLASSIFIER = cv.CascadeClassifier(config.FACE_CASCADE)


def face_positions(img):
    return CASCADE_CLASSIFIER.detectMultiScale(img, scaleFactor=1.5, minNeighbors=5)


def detect_face(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_img = cv.equalizeHist(gray_img)

    faces = face_positions(gray_img)

    if len(faces) != 1:
        return None

    x, y, w, h = faces[0]
    face_roi = gray_img[y:y + h, x:x + w]
    face_roi = cv.resize(face_roi, config.FACE_SIZE, interpolation=cv.INTER_AREA)

    return face_roi


def camera_read(frames_limit: int = 0, time_limit: float = 0, show_frames=True):
    cap = cv.VideoCapture(config.DEFAULT_CAMERA)

    unlim_frames = True if frames_limit > 0 else False
    unlim_time = True if time_limit > 0 else False

    frame_count, time_start = 0, time.perf_counter()

    while (unlim_frames or frame_count < frames_limit) and (unlim_time or time.perf_counter() - time_start > 0):
        _, frame = cap.read()

        yield frame

        if show_frames:
            faces = face_positions(frame)
            for x, y, w, h in faces:
                blue, stroke = (255, 0, 0), 2
                cv.rectangle(frame, (x, y), (x + w, y + h), blue, stroke)

            cv.imshow('User ID', frame)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break

