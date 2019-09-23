from priorityqueue import PriorityQueue
from random import randint
from bookcharacter import *

if __name__ == '__main__':
    qu = PriorityQueue()

    books = [Book(f'{chr(randint(65, 90))}{chr(randint(97, 122))}', [f'{chr(randint(65, 90))}',
             f'{randint(65, 90)}'], randint(-40, 1920), randint(3, 9821), f'annotation{i}') for i in range(20)]

    prices = [randint(3, 582) for _ in range(20)]

    for pair in zip(books, prices):
        qu.put(pair)

    random_character = BookCharacter(['randomist'], [])

    while qu:
        book, price = qu.get()
        print(book)
        random_character.add_book(book, CharacterRole(price % 3))

    print(random_character)
    print(repr(random_character))