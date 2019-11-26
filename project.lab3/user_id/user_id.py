import os
import config


class UserID:
    def __init__(self, username: str):
        self.username = username

        user_dir = UserID.user_dir(username)
        password_path = user_dir + 'password.txt'
        trainer_path = user_dir + 'trainer.yml'

        with open(password_path, 'r') as pswd:
            self.password = pswd.readline()

        if os.path.exists(trainer_path):
            self.recognizer = config.CREATE_RECOGNIZER()
            self.recognizer.read(trainer_path)
        else:
            self.recognizer = None

    @classmethod
    def register(cls, username: str, password: str):
        user_dir = cls.user_dir(username)

        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
            with open(user_dir + 'password.txt', 'w') as pswd:
                pswd.write(password)

            return cls(username)
        else:
            raise FileExistsError(f'Username {username} exists already')

    def face_unlock(self, face: 'grayscale img'):
        if self.recognizer is None:
            raise BaseException

        _, distance = self.recognizer.predict(face)

        if distance < 45:
            return True

        return False

    def password_unlock(self, password: str):
        return self.password == password

    @staticmethod
    def user_dir(username: str):
        return config.USERS_DIR + username + '/'

