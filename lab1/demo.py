import random
import string
from priorityqueue import PriorityQueue
from bookcharacter import *

RAND_SEQ_SIZE_BOTTOM = 3
RAND_SEQ_SIZE_TOP = 12


def random_str():
    length = random.randint(RAND_SEQ_SIZE_BOTTOM, RAND_SEQ_SIZE_TOP)
    return random.choice(string.ascii_uppercase) + \
           ''.join(random.choice(string.ascii_lowercase) for _ in range(1, length))


def random_int():
    return random.randint(10, 1_000_000)


def random_list():
    length = random.randint(RAND_SEQ_SIZE_BOTTOM, RAND_SEQ_SIZE_TOP)
    return [random.choice([random_int, random_str])() for _ in range(length)]


def random_tuple():
    return tuple(random_list())


def random_book():
    authors_number = random.randint(1, 3)
    return Book(random_str(), [random_str() for _ in range(authors_number)], random.randint(0, 2000),
                random.randint(0, 10_000), random_str())


def random_book_character():
    books_number = random.randint(1, 3)
    names_number = random.randint(1, 3)
    return BookCharacter([random_str() for _ in range(names_number)],
                         [(random_book(), CharacterRole(random.randint(0, 2))) for _ in range(books_number)])


def random_obj():
    return random.choice([random_str, random_int, random_list, random_tuple, random_book, random_book_character])()


def demo_basic():
    qu = PriorityQueue()

    books = [Book(random_str(), [random_str(), random_str()], random.randint(-40, 1920),
                  random.randint(3, 9821), random_str()) for _ in range(20)]

    prices = [random.randint(3, 582) for _ in range(20)]

    for pair in zip(books, prices):
        qu.put(pair)

    random_character = BookCharacter(['random character'], [])

    while qu:
        book, price = qu.get()
        print(book)
        random_character.add_book(book, CharacterRole(price % 3))

    print(random_character)
    print(repr(random_character))


def demo_priority_queue():
    print('DEMO OF USING PRIORITY QUEUE WITH DIFFERENT TYPES')

    key_type = random.choice([random_int, random_str])
    puts_num = random.randint(20, 30)
    gets_num = random.randint(5, puts_num - 1)

    pq = PriorityQueue()
    print('PRIORITY QUEUE CURRENT STATE: ')
    print(pq)

    for _ in range(puts_num):
        key, obj = key_type(), random_obj()

        print()
        print(f'PUT KEY={key}, OBJECT={obj}')
        pq.put((key, obj))

        print('PRIORITY QUEUE CURRENT STATE: ')
        print(pq)

    for _ in range(gets_num):
        key, obj = pq.get()
        print()
        print(f'GET KEY={key}, OBJECT={obj}')
        print('PRIORITY QUEUE CURRENT STATE: ')
        print(pq)
