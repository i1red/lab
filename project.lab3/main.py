import numpy as np
from face_rec import cam_tools
from face_rec import user_id


def create_training(frames_number):
    training = []
    for img in cam_tools.camera_read(frames_limit=frames_number):
        face = cam_tools.detect_face(img)

        if face is not None:
            training.append(np.array(face, 'uint8'))

    return training


if __name__ == '__main__':
    password = '12345'
    ivan = user_id.UserID.register('ivan2', password)
    ivan.create_recognizer(create_training(50))

    unlocked_with_face = False
    for img in cam_tools.camera_read(time_limit=3):
        face = cam_tools.detect_face(img)

        if face is not None:
            unlocked_with_face = ivan.face_unlock(face)

        if unlocked_with_face:
            break

    if unlocked_with_face:
        print(f'Recognized {ivan.username}')

    print(ivan.password_unlock('121'))
    print(ivan.password_unlock(password))


