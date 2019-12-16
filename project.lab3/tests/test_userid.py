import unittest
import uuid
from face_rec.userid import UserID


class TestUserID(unittest.TestCase):
    def setUp(self) -> None:
        self.test_username = uuid.uuid4().hex
        self.test_password = uuid.uuid4().hex
        UserID.register(self.test_username, self.test_password)

    def tearDown(self) -> None:
        UserID.delete(self.test_username)

    def test_password_unlock_false(self):
        password = uuid.uuid4().hex
        while password == self.test_password:
            password = uuid.uuid4().hex

        user = UserID(self.test_username)
        self.assertFalse(user.password_unlock(password))

    def test_password_unlock_true(self):
        user = UserID(self.test_username)
        self.assertTrue(user.password_unlock(self.test_password))

    def test_has_recognizer_false(self):
        user = UserID(self.test_username)
        self.assertFalse(user.has_recognizer())

    def test_has_recognizer_true(self):
        user = UserID(self.test_username)
        user.create_recognizer()
        self.assertTrue(user.has_recognizer())

if __name__ == '__main__':
    unittest.main()