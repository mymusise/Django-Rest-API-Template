"""
All thing about crypt and decrypt
"""


EASY_IDENTIFIED_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz"


def basex_encode(num, alphabet=EASY_IDENTIFIED_ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    assert num >= 0
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num //= base
        arr.append(alphabet[rem])
    arr.reverse()
    return "".join(arr)


def basex_decode(string, alphabet=EASY_IDENTIFIED_ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = strlen - (idx + 1)
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num
