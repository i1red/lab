from datetime import date

class Book:
    def __init__(self, title: str, authors: tuple, release_date: date, size: int, annotation: str):
        self._title = title
        self._authors = authors
        self._release_date = release_date
        self._size = size
        self._annotation = annotation


    @property
    def title(self):
        return self._title


    @property
    def authors(self):
        return self._authors


    @property
    def release_date(self):
        return self._release_date


    @property
    def size(self):
        return self._size

    @property
    def annotation(self):
        return self._annotation


    def __repr__(self):
        return f'Book({repr(self.title)}, {repr(self.authors)}, ' \
            f'{repr(self.release_date)}, {self.size}, {repr(self.annotation)})'


    def __str__(self):
        return f'Book "{self.title}" written by {self.authors}. Released on {self.release_date}. {self.size} pages. ' \
            f'About: {self.annotation}'

a = Book('wwww', ('131', 'wcwe'), date(1291, 2, 12), 121, '')
print(a)