
import re
import os
import sourcemap

from typing import Dict, List


class SourceMap:
    '''Map (line, column) pairs from generated to source file.'''

    def __tmp5(__tmp0, __tmp3: List[str]) -> None:
        __tmp0._dirs = __tmp3
        __tmp0._indices = {}  # type: Dict[str, sourcemap.SourceMapDecoder]

    def _index_for(__tmp0, __tmp4: <FILL>) :
        '''Return the source map index for minified_src, loading it if not
           already loaded.'''
        if __tmp4 not in __tmp0._indices:
            for source_dir in __tmp0._dirs:
                filename = os.path.join(source_dir, __tmp4 + '.map')
                if os.path.isfile(filename):
                    with open(filename) as fp:
                        __tmp0._indices[__tmp4] = sourcemap.load(fp)
                        break

        return __tmp0._indices[__tmp4]

    def __tmp1(__tmp0, __tmp2) -> str:
        out = ''  # type: str
        for ln in __tmp2.splitlines():
            out += ln + '\n'
            match = re.search(r'/static/(?:webpack-bundles|min)/(.+)(\.[\.0-9a-f]+\.js):(\d+):(\d+)', ln)
            if match:
                # Get the appropriate source map for the minified file.
                __tmp4 = match.groups()[0] + match.groups()[1]
                index = __tmp0._index_for(__tmp4)

                gen_line, gen_col = list(map(int, match.groups()[2:4]))
                # The sourcemap lib is 0-based, so subtract 1 from line and col.
                try:
                    result = index.lookup(line=gen_line-1, column=gen_col-1)
                    display_src = result.src
                    webpack_prefix = "webpack:///"
                    if display_src.startswith(webpack_prefix):
                        display_src = display_src[len(webpack_prefix):]
                    out += ('       = %s line %d column %d\n' %
                            (display_src, result.src_line+1, result.src_col+1))
                except IndexError:
                    out += '       [Unable to look up in source map]\n'

            if ln.startswith('    at'):
                out += '\n'
        return out
