import unittest
import random
from demo import random_book
from bookcharacter import *


class TestBookCharacter(unittest.TestCase):
    def setUp(self) -> None:
        self.ref_books = [(Book('Exam cheating', ['Students'], 1972, 10758, "When session comes"),
                           CharacterRole.MAIN),
                          (Book('Lack of sleeping', ['People over 10'], 1421, 23, 'zzzzzzZZZZ...'),
                           CharacterRole.MAIN),
                          (Book('Studying', ['Straight A students'], 2009, 12121, 'OOP, algorithms'),
                           CharacterRole.FLAT)]
        self.vanya_names = ['Vanya', 'Nice fellow']
        self.vanya = BookCharacter(self.vanya_names, self.ref_books)

    def test_init(self):
        initial_names = ['Luchano', 'Luigi']
        initial_books = [(Book('test book', ['test author'], 22, 1, 'tralala'), CharacterRole.FLAT)]
        luchano = BookCharacter(initial_names, initial_books)

        self.assertEqual(luchano.names, initial_names)
        self.assertEqual(luchano.referred_books, initial_books)

    def test_add_book(self):
        lotr = [(Book('LOTR: The Fellowship of the Ring', ['J. R. R. Tolkien'], 1954, 479, '1st part'),
                 CharacterRole.MAIN),
                (Book('LOTR: The Two Towers', ['J. R. R. Tolkien'], 1954, 372, '2nd part'),
                 CharacterRole.MAIN),
                (Book('LOTR: The Return of the King', ['J. R. R. Tolkien'], 1955, 487, '3rd part'),
                 CharacterRole.MAIN)]

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
        expected_str_vanya = 'Book character, known as Vanya, Nice fellow. ' \
                       'Referred books: "Exam cheating" by Students; "Lack of sleeping" by People over 10; ' \
                       '"Studying" by Straight A students'

        self.assertEqual(str(self.vanya), expected_str_vanya)

    def test_repr(self):
        expected_repr1_vanya = f'BookCharacter([\'Vanya\', \'Nice fellow\'], [{reprlib.repr(self.ref_books[0])}, ' \
                               f'{reprlib.repr(self.ref_books[1])}, ...])'

        self.assertEqual(expected_repr1_vanya, repr(self.vanya))

    def test_serialize_books(self):
        random_books = []
        expected_books = []

        for _ in range(20):
            book = random_book()

            role = random.randint(0, 2)

            if role >= 1:
                expected_books.append(book)

            random_books.append((book, CharacterRole(role)))

        julia = BookCharacter(['Julia'], random_books)
        self.assertEqual(julia.serialize_books(), expected_books)


if __name__ == '__main__':
    unittest.main()
