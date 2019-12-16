import unittest
import uuid
from face_rec.userid import UserID
from face_rec.imgtools import folder_read, detect_face


class TestBasicUserID(unittest.TestCase):
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


class TestFaceUnlockWilder(unittest.TestCase):
    def setUp(self) -> None:
        self.user = UserID('wilder')
        self.incorrect_variants = ['trump', 'ivan']

    def test_face_unlock_false(self):
        for variant in self.incorrect_variants:
            self.assertFalse(self.user.face_unlock_img_seq(folder_read(f'photos/{variant}')))

    def test_face_unlock_true(self):
        all_photos = unlocked_photos = 0

        for img in folder_read(f'photos/{self.user.username}'):
            face = detect_face(img)
            if face is not None:
                all_photos += 1
                if self.user.face_unlock(face):
                    unlocked_photos += 1

        expected_percentage = 0.5
        self.assertGreater(unlocked_photos / all_photos, expected_percentage)


class TestFaceUnlockTrump(TestFaceUnlockWilder):
    def setUp(self) -> None:
        self.user = UserID('trump')
        self.incorrect_variants = ['wilder', 'ivan']


class TestFaceUnlockIvan(TestFaceUnlockWilder):
    def setUp(self) -> None:
        self.user = UserID('ivan')
        self.incorrect_variants = ['wilder', 'trump']


if __name__ == '__main__':
    unittest.main()