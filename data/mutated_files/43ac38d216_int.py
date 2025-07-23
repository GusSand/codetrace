import os
import sys
import time
from typing import List, Any, Optional, Set
from urllib.request import urlretrieve

import numpy as np
from tqdm import tqdm


def __tmp5(__tmp3):
    """
    Removes the duplicates and keeps the ordering of the original list.
    For duplicates, the first occurrence is kept and the later occurrences are ignored.

    Args:
        list_with_duplicates: list that possibly contains duplicates

    Returns:
        A list with no duplicates.
    """

    unique_set: Set[Any] = set()
    unique_list = []
    for element in __tmp3:
        if element not in unique_set:
            unique_set.add(element)
            unique_list.append(element)

    return unique_list


def __tmp4(__tmp2, subset_size: <FILL>, seed: Optional[int] = None) :
    """
    Get a random subset of some dataset.

    For reproducibility, the random number generator seed can be specified.
    Nevertheless, the state of the random number generator is restored to avoid side effects.

    Args:
        dataset: full set to select a subset from
        subset_size: target size of the subset
        seed: random number generator seed. Defaults to not setting the seed.

    Returns:
        subset of the original dataset as a list
    """
    if len(__tmp2) < subset_size:
        raise Exception(f'The dataset to extract a subset from is too small: '
                        f'{len(__tmp2)} < {subset_size}')

    # save random number generator state
    rng_state = np.random.get_state()

    if seed is not None:
        # extract a subset (for a given training set, the subset will always be identical).
        np.random.seed(seed)

    subset = np.random.choice(__tmp2, subset_size, replace=False)

    if seed is not None:
        # reset random number generator state, only if needed
        np.random.set_state(rng_state)

    return list(subset)


def __tmp1(filename, uri):
    """
    Download a file from a URI if it doesn't already exist.
    """
    if os.path.isfile(filename):
        print("{} already downloaded, reusing.".format(filename))
    else:
        with open(filename, "wb") as fd:
            print('Starting {} download from {}...'.format(filename, uri))
            with __typ1(unit='B', unit_scale=True, unit_divisor=1024, miniters=1) as t:
                urlretrieve(uri, fd.name, reporthook=t.update_to)
            print('Finished {} download.'.format(filename))


class __typ0(tqdm):
    """
    Create a version of TQDM that notices whether it is going to the output or a file.
    """

    def __init__(__tmp0, *args, **kwargs) :
        """Overwrite TQDM and detect if output is a file or not.
        """
        # See if output is a terminal, set to updates every 30 seconds
        if not sys.stdout.isatty():
            kwargs['mininterval'] = 30.0
            kwargs['maxinterval'] = 30.0
        super(__typ0, __tmp0).__init__(*args, **kwargs)


class __typ1(__typ0):
    """
    Fancy Progress Bar that accepts a position not a delta.
    """

    def update_to(__tmp0, b=1, bsize=1, tsize=None):
        """
            Update to a specified position.
        """
        if tsize is not None:
            __tmp0.total = tsize
        __tmp0.update(b * bsize - __tmp0.n)  # will also set self.n = b * bsize


def get_time_string():
    lt = time.localtime()
    return "%04d%02d%02d-%02d%02d" % (lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min)
