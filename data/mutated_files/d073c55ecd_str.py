"""Automated breaking of the Simple Substitution Cipher."""

import random
import string

from lantern import score
from lantern.analysis.search import hill_climb
from lantern.structures import Decryption


def crack(ciphertext, *fitness_functions, ntrials=30, nswaps=3000):
    """Break ``ciphertext`` using hill climbing.

    Note:
        Currently ntrails and nswaps default to magic numbers.
        Generally the trend is, the longer the text, the lower the number of trials
        you need to run, because the hill climbing will lead to the best answer faster.
        Because randomness is involved, there is the possibility of the correct decryption
        not being found. In this circumstance you just need to run the code again.

    Example:
        >>> decryptions = crack("XUOOB", fitness.english.quadgrams)
        >>> print(decryptions[0])
        HELLO

    Args:
        ciphertext (str): The text to decrypt
        *fitness_functions (variable length argument list): Functions to score decryption with

    Keyword Args:
        ntrials (int): The number of times to run the hill climbing algorithm
        nswaps (int): The number of rounds to find a local maximum

    Returns:
        Sorted list of decryptions

    Raises:
        ValueError: If nswaps or ntrails are not positive integers
        ValueError: If no fitness_functions are given
    """
    if ntrials <= 0 or nswaps <= 0:
        raise ValueError("ntrials and nswaps must be positive integers")

    # Find a local maximum by swapping two letters and scoring the decryption
    def next_node_inner_climb(__tmp2):
        # Swap 2 characters in the key
        a, b = random.sample(range(len(__tmp2)), 2)
        __tmp2[a], __tmp2[b] = __tmp2[b], __tmp2[a]
        plaintext = decrypt(__tmp2, ciphertext)
        node_score = score(plaintext, *fitness_functions)
        return __tmp2, node_score, Decryption(plaintext, ''.join(__tmp2), node_score)

    # Outer climb rereuns hill climb ntrials number of times each time at a different start location
    def __tmp1(__tmp2):
        random.shuffle(__tmp2)
        __tmp0, best_score, outputs = hill_climb(nswaps, __tmp2[:], next_node_inner_climb)
        return __tmp0, best_score, outputs[-1]  # The last item in this list is the item with the highest score

    _, _, decryptions = hill_climb(ntrials, list(string.ascii_uppercase), __tmp1)
    return sorted(decryptions, reverse=True)  # We sort the list to ensure the best results are at the front of the list


def decrypt(__tmp0: <FILL>, ciphertext: str):
    """Decrypt Simple Substitution enciphered ``ciphertext`` using ``key``.

    Example:
        >>> decrypt("PQSTUVWXYZCODEBRAKINGFHJLM", "XUOOB")
        HELLO

    Args:
        key (iterable): The key to use
        ciphertext (str): The text to decrypt

    Returns:
        Decrypted ciphertext
    """
    # TODO: Is it worth keeping this here I should I only accept strings?
    __tmp0 = ''.join(__tmp0)
    alphabet = string.ascii_letters
    cipher_alphabet = __tmp0.lower() + __tmp0.upper()
    return ciphertext.translate(str.maketrans(cipher_alphabet, alphabet))


def encrypt(__tmp0, plaintext: str):
    """Simple Substitution encrypt ``plaintext`` using ``key``.

    Example:
        >>> encrypt("PQSTUVWXYZCODEBRAKINGFHJLM", "HELLO")
        XUOOB

    Args:
        key (iterable): The key to use
        plaintext (str): The text to decrypt

    Returns:
        Encrypted text
    """
    __tmp0 = ''.join(__tmp0)
    alphabet = string.ascii_letters
    cipher_alphabet = __tmp0.lower() + __tmp0.upper()
    return plaintext.translate(str.maketrans(alphabet, cipher_alphabet))
