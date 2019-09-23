import unittest
import random
import string
from lab1.bookcharacter import *


class TestBookCharacter(unittest.TestCase):
    def setUp(self) -> None:
        self.ref_books = [(Book('Exam cheating', ['Students'], 1972, 10758, "Describes student's life when session comes"),
                           CharacterRole.MAIN),
                          (Book('Lack of sleeping', ['People over 10'], 1421, 23, 'zzzzzzZZZZ...'),
                           CharacterRole.MAIN),
                          (Book('Studying', ['Straight A students', 'I do not know who else'], 2009, 12121,
                           'OOP fundamentals, algorithms and extreme complexity...'), CharacterRole.FLAT)]
        self.vanya_names = ['Vanya', 'Guy who doing labs', 'Nice fellow']
        self.vanya = BookCharacter(self.vanya_names, self.ref_books)

    def test_init(self):
        initial_names = ['Luchano', 'Luigi']
        initial_books = [(Book('test book', ['test author'], 22, 1, 'tralala'), CharacterRole.FLAT)]
        luchano = BookCharacter(initial_names, initial_books)
        self.assertEqual(luchano.names, initial_names)
        self.assertEqual(luchano.referred_books, initial_books)

    def test_add_book(self):
        lotr = [(Book('The Lord of the Rings: The Fellowship of the Ring', ['J. R. R. Tolkien'], 1954, 479,
                     'The first part of a legendary trilogy'), CharacterRole.MAIN),
                (Book('The lord of the Rings: The Two Towers', ['J. R. R. Tolkien'], 1954, 372,
                     'The second part of a legendary trilogy'), CharacterRole.MAIN),
                (Book('The lord of the Rings: The Return of the King', ['J. R. R. Tolkien'], 1955, 487,
                     'The third part of a legendary trilogy'), CharacterRole.MAIN)]

        aragorn = BookCharacter(['Aragorn'], [lotr[0]])
        aragorn.add_book(*lotr[1])
        aragorn.add_book(*lotr[2])
        self.assertEqual(aragorn.referred_books, lotr)

    def test_add_name(self):
        names = ['Lord Snow', 'Aegon Targaryen', 'The White Wolf']
        jon_snow = BookCharacter(['Jon Snow'], [(Book('A Song of Ice and Fire', ['George R. R. Martin'],
                                 1996, 4228, 'Series of epic fantasy novels'), CharacterRole.MAIN)])

        for name in names:
            jon_snow.add_name(name)

        expected_names = ['Jon Snow', 'Lord Snow', 'Aegon Targaryen', 'The White Wolf']
        self.assertEqual(jon_snow.names, expected_names)

    def test_str(self):
        expected_str_vanya = 'Book character, known as Vanya, Guy who doing labs, Nice fellow. ' \
                       'Referred books: "Exam cheating" by Students; "Lack of sleeping" by People over 10; ' \
                       '"Studying" by Straight A students, I do not know who else'

        self.assertEqual(str(self.vanya), expected_str_vanya)

    def test_repr(self):
        expected_repr1_vanya = f'BookCharacter([\'Vanya\', \'Guy who doing labs\', ...], [{reprlib.repr(self.ref_books[0])}, ' \
                               f'{reprlib.repr(self.ref_books[1])}, ...])'

        self.assertEqual(repr(self.vanya), expected_repr1_vanya)

    def test_serialize_books(self):
        random_books = []
        expected_books = []

        random_str = lambda l: random.choice(string.ascii_uppercase) + ''.join(string.ascii_lowercase for _ in range(l))

        for _ in range(20):
            title_len = random.randint(3, 50)
            title = random_str(title_len)

            authors_number = random.randint(1, 3)
            authors = [random_str(random.randint(5, 20)) for _ in range(authors_number)]

            release_year = random.randint(-300, 2019)

            size = random.randint(28, 6821)

            annotation_len = random.randint(0, 80)
            annotation = random_str(annotation_len)

            book = Book(title, authors, release_year, size, annotation)

            role = random.randint(0, 2)

            if role >= 1:
                expected_books.append(book)

            random_books.append((book, CharacterRole(role)))

        julia = BookCharacter(['Julia'], random_books)
        self.assertEqual(julia.serialize_books(), expected_books)


if __name__ == '__main__':
    unittest.main()
