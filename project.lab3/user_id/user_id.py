import os
import config


class UserID:
    def __init__(self, username):
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
    def register(cls, username, password):
        user_dir = cls.user_dir(username)

        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
            with open(user_dir + 'password.txt', 'w') as pswd:
                pswd.write(password)

            return cls(username)
        else:
            raise FileExistsError(f'Username {username} exists already')

    @staticmethod
    def user_dir(username):
        return config.USERS_DIR + username + '/'

