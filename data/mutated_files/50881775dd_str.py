from typing import TypeAlias
__typ0 : TypeAlias = "Pair"
import logging
from os.path import isfile
from os.path import join
from parser.pair import Pair
from parser.parser_base import ParserBase
from typing import Dict
from typing import Iterable


class PairParser(ParserBase):

    def __tmp3(__tmp0, pairs_fname: <FILL>, __tmp5) :
        __tmp0.pairs_fname = pairs_fname
        __tmp0._image_dir = __tmp5

    def __tmp4(__tmp0) :
        with open(__tmp0.pairs_fname, 'r', encoding='utf-8') as f:
            next(f)  # pylint: disable=stop-iteration-return
            # skip first line, which contains metadata
            for __tmp1 in f:
                try:
                    pair = __tmp0._compute_pair(__tmp1)
                except FileNotFoundError:
                    logging.exception('Skipping invalid file')
                else:
                    yield pair

    def __tmp2(__tmp0) :
        raise NotImplementedError()

    def _compute_full_path(__tmp0, image_path) :
        exts = ['.jpg', '.png']
        for ext in exts:
            full_image_path = join(__tmp0._image_dir, f'{image_path}{ext}')
            if isfile(full_image_path):
                return full_image_path
        err = f'{image_path} does not exist with extensions: {exts}'
        raise FileNotFoundError(err)

    def _compute_pair(__tmp0, __tmp1) :
        line_info = __tmp1.strip().split()
        if len(line_info) == 3:
            name, n1, n2 = line_info
            image1 = __tmp0._compute_full_path(join(name,
                                                  f'{name}_{int(n1):04d}'))
            image2 = __tmp0._compute_full_path(join(name,
                                                  f'{name}_{int(n2):04d}'))
            is_match = True
        else:
            name1, n1, name2, n2 = line_info
            image1 = __tmp0._compute_full_path(join(name1,
                                                  f'{name1}_{int(n1):04d}'))
            image2 = __tmp0._compute_full_path(join(name2,
                                                  f'{name2}_{int(n2):04d}'))
            is_match = False
        return __typ0(image1, image2, is_match)
