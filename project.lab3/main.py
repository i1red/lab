from face_rec.imgtools import camera_read, detect_face
from face_rec.userid import UserID, create_training
from uuid import uuid4


def demo_create_user(frame_count_trainer, time_to_recognize):
    user = UserID.register(uuid4().hex, uuid4().hex)
    user.create_recognizer(create_training(camera_read(frames_limit=frame_count_trainer)))

    print('Recognized' if user.face_unlock_img_seq(camera_read(time_limit=time_to_recognize)) else 'Not recognized')

    UserID.delete(user.username)


if __name__ == '__main__':
    demo_create_user(30, 5)