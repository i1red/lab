import numpy as np
from face_rec import imgtools
from face_rec import userid



if __name__ == '__main__':
    trump = userid.UserID('trump')
    for img in imgtools.folder_read('tests/photos/trump/'):
        face = imgtools.detect_face(img)
        if face is not None:
            print(trump.face_unlock(face))


