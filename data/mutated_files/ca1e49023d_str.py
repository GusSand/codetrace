
import re
import os
import sourcemap

from typing import Dict, List


class SourceMap:
    '''Map (line, column) pairs from generated to source file.'''

    def __init__(__tmp1, sourcemap_dirs) -> None:
        __tmp1._dirs = sourcemap_dirs
        __tmp1._indices = {}  # type: Dict[str, sourcemap.SourceMapDecoder]

    def _index_for(__tmp1, __tmp2: str) :
        '''Return the source map index for minified_src, loading it if not
           already loaded.'''
        if __tmp2 not in __tmp1._indices:
            for source_dir in __tmp1._dirs:
                filename = os.path.join(source_dir, __tmp2 + '.map')
                if os.path.isfile(filename):
                    with open(filename) as fp:
                        __tmp1._indices[__tmp2] = sourcemap.load(fp)
                        break

        return __tmp1._indices[__tmp2]

    def __tmp0(__tmp1, stacktrace: <FILL>) -> str:
        out = ''  # type: str
        for ln in stacktrace.splitlines():
            out += ln + '\n'
            match = re.search(r'/static/(?:webpack-bundles|min)/(.+)(\.[\.0-9a-f]+\.js):(\d+):(\d+)', ln)
            if match:
                # Get the appropriate source map for the minified file.
                __tmp2 = match.groups()[0] + match.groups()[1]
                index = __tmp1._index_for(__tmp2)

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
