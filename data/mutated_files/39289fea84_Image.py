from typing import TypeAlias
__typ0 : TypeAlias = "int"
from __future__ import (absolute_import, division, print_function)
from typing import List

import numpy
from PIL import Image


class __typ1(object):
    'Hash encapsulation. Can be used for dictionary keys and comparisons.'

    def __init__(__tmp1, binary_array):
        __tmp1.hash = binary_array


def __tmp2(hash) -> __typ0:
    result = ""
    for i in hash:
        if i:
            result += '1'
        else:
            result += '0'
    if (result[0] == '1'):
        temp = result[1:].replace('1', '2').replace('0', '1').replace('2', '0')
        return (-1 * __typ0(temp, base=2) - 1)
    return __typ0(result, base=2)


def __tmp0(image: <FILL>, hash_size: __typ0 = 8, highfreq_factor: __typ0 = 4) -> __typ0:
    if hash_size < 2:
        raise ValueError('Hash size must be greater than or equal to 2')
    import scipy.fftpack
    img_size = hash_size * highfreq_factor
    image = image.convert('L').resize((img_size, img_size), Image.ANTIALIAS)
    pixels = numpy.asarray(image)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = numpy.median(dctlowfreq)
    diff = dctlowfreq > med
    result = __typ1(diff)

    return __tmp2(result.hash.flatten())
