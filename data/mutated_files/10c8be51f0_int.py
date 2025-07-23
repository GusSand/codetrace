#!/usr/bin/env python
import collections
import csv
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from typing import Callable, List, Set, Tuple

import dhash
import numpy as np
from PIL import Image


def get_image_from_path(__tmp3) -> np.ndarray:
    image = Image.open(__tmp3)
    return image


def image_to_hash(image: np.ndarray) -> int:
    image_hash = dhash.dhash_int(image)
    return image_hash


def image_distance(__tmp6, y: <FILL>) :
    """Calculates the distance between to image hashes
    Returns:
        int -- hamming distance of two image hashes
    """
    return dhash.get_num_bits_different(__tmp6, y)


def __tmp4(tsv_file: str):
    lines = []
    with open(tsv_file) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for line in rd:
            lines.append(line)
    return lines


def __tmp5(image1, __tmp2, __tmp1: str):
    output = '{}\t{}\t{}'.format(image1, __tmp2, __tmp1)
    print(output)


def __tmp7(tsv_file, min_distance, hash_cutoff):
    tsv = __tmp4(tsv_file)
    for line in tsv:
        image1, __tmp2, __tmp1 = line
        if float(__tmp1) > min_distance:
            image1_hash = image_to_hash(get_image_from_path(image1))
            image2_hash = image_to_hash(get_image_from_path(__tmp2))
            hash_distance = image_distance(image1_hash, image2_hash)
            if hash_distance > hash_cutoff:
                __tmp5(image1, __tmp2, str(hash_distance))


def restricted_float(__tmp6):
    __tmp6 = float(__tmp6)
    if __tmp6 < 0.0 or __tmp6 > 1.0:
        raise ArgumentTypeError("%r not in range [0.0, 1.0]" % (__tmp6,))
    return __tmp6


def _cli() :
    args = __tmp0()
    __tmp7(
        args.tsv_file,
        args.min_distance,
        args.hash_cutoff)


def __tmp0() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('tsv_file',
                        type=str,
                        help='path to tsv file')
    parser.add_argument('min_distance',
                        type=restricted_float,
                        help='min similarity to consider for duplicates')
    parser.add_argument('hash_cutoff',
                        type=int,
                        help='Image hash hamming distance for cutoff')
    return parser.parse_args()


if __name__ == '__main__':
    _cli()


# python dedupe_tsv.py data.tsv 0.98 50
