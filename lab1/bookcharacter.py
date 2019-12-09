from collections import namedtuple
from enum import Enum
import reprlib

Book = namedtuple('Book', ['title', 'authors', 'release_date', 'size', 'annotation'])


class CharacterRole(Enum):
    FLAT = 0
    SECONDARY = 1
    MAIN = 2


class BookCharacter:
    def __init__(self, names: list, reffered_books: list):
        self._names = list(names)
        self._reffered_books = [(book, role) for book, role in reffered_books]

    def __repr__(self):
        return f'BookCharacter({reprlib.repr(self._names)}, {reprlib.repr(self._reffered_books)})'

    def __str__(self):
        ref_books_str = [f'''"{book.title}" by {', '.join(book.authors)}'''  for book, role in self._reffered_books]
        return f"Book character, known as {', '.join(self.names)}. Reffered books: {'; '.join(ref_books_str)}"

    @property
    def names(self):
        return list(self._names)

    @property
    def reffered_books(self):
        return list(self._reffered_books)

    def add_name(self, name: str):
        self._names.append(name)

    def add_book(self, reffered_book: Book, role):
        self._reffered_books.append((reffered_book, role))

    def serialize_books(self):
        return [book for book, role in self._reffered_books
                if role == CharacterRole.SECONDARY or role == CharacterRole.MAIN]
