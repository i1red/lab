import os
import numpy as np
import config


class UserID:
    def __init__(self, username: str):
        self.username = username

        user_dir = UserID._user_dir(username)
        self._pswd_file = user_dir + 'password.txt'
        self._trainer_file = user_dir + 'trainer.yml'

        with open(self._pswd_file, 'r') as pswd:
            self._password = pswd.readline()

        if os.path.exists(self._trainer_file):
            self._recognizer = config.CREATE_RECOGNIZER()
            self._recognizer.read(self._trainer_file)
        else:
            self._recognizer = None

    @classmethod
    def register(cls, username: str, password: str):
        user_dir = cls._user_dir(username)

        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
            with open(user_dir + 'password.txt', 'w') as pswd:
                pswd.write(password)

            return cls(username)
        else:
            raise FileExistsError(f'Username {username} exists already')

    def has_recognizer(self):
        pass

    def remove_recognizer(self):
        self._recognizer = None

    def update_recognizer(self, training: 'list of 2d arrays'):
        ids = np.array([0 for _ in range(len(training))])
        self._recognizer.update(training, ids)
        self._recognizer.save()

    def face_unlock(self, face: 'grayscale img'):
        if self._recognizer is None:
            raise BaseException

        _, distance = self._recognizer.predict(face)

        if distance < 45:
            return True

        return False

    def password_unlock(self, password: str):
        return self._password == password

    @staticmethod
    def _user_dir(username: str):
        return config.USERS_DIR + username + '/'

