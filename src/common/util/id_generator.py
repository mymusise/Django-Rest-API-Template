import datetime
import random
import string
import time

from .crypt import basex_encode


class Id40Generator:
    ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase

    def __init__(self, date_str, alphabet=None):
        self.since = time.mktime(
            datetime.datetime.strptime(date_str, '%Y-%m-%d').timetuple())
        if alphabet:
            self.alphabet = alphabet
        else:
            self.alphabet = self.ALPHABET

    def __time_since(self, timestamp=None):
        if timestamp:
            time_since = int(timestamp - self.since)
        else:
            time_since = int(time.time() - self.since)
        return time_since

    def gen_id(self, timestamp=None):
        return basex_encode((self.__time_since(timestamp) << 9)
                            + random.SystemRandom().getrandbits(9),
                            self.alphabet)


class RandomStringGenerator:

    def __init__(self, length, alphabet=string.ascii_uppercase):
        self.length = length
        self.alphabet = alphabet

    def gen_id(self):
        return ''.join(random.choices(self.alphabet, k=self.length))
