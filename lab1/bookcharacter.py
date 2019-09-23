from collections import namedtuple
from enum import Enum
import reprlib

Book = namedtuple('Book', ['title', 'authors', 'release_year', 'size', 'annotation'])


class CharacterRole(Enum):
    FLAT = 0
    SECONDARY = 1
    MAIN = 2


class BookCharacter:
    def __init__(self, names: list, referred_books: list):
        self._names = list(names)
        self._referred_books = [(book, role) for book, role in referred_books]

    def __repr__(self):
        special_repr = reprlib.Repr()
        special_repr.maxlist = 2
        return f'BookCharacter({special_repr.repr(self._names)}, {special_repr.repr(self._referred_books)})'

    def __str__(self):
        ref_books_str = [f'''"{book.title}" by {', '.join(book.authors)}''' for book, role in self._referred_books]
        return f"Book character, known as {', '.join(self.names)}. Referred books: {'; '.join(ref_books_str)}"

    @property
    def names(self):
        return list(self._names)

    @property
    def referred_books(self):
        return list(self._referred_books)

    def add_name(self, name: str):
        self._names.append(name)

    def add_book(self, reffered_book: Book, role):
        self._referred_books.append((reffered_book, role))

    def serialize_books(self):
        return [book for book, role in self._referred_books
                if role == CharacterRole.SECONDARY or role == CharacterRole.MAIN]