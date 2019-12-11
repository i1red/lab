import random
import string
from bookcharacter import *


RAND_SEQ_SIZE_BOTTOM = 3
RAND_SEQ_SIZE_TOP = 12


def random_str():
    length = random.randint(RAND_SEQ_SIZE_BOTTOM, RAND_SEQ_SIZE_TOP)
    return random.choice(string.ascii_uppercase) + ''.join(string.ascii_lowercase for _ in range(1, length))


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
    return random.choice([random_str, random_int, random_list, random_tuple, random_book, random_book_character])