from typing import TypeAlias
__typ0 : TypeAlias = "str"
from functools import partial
from parser.container_parser import ContainerParser
from parser.face_vector_parser import FaceVectorParser
from parser.pipeline.parser_pipeline import ParserPipeline
from parser.pipeline.parser_pipeline_funcs import fill_empty
from parser.pipeline.parser_pipeline_funcs import filter_target


class FaceVectorFillParser(FaceVectorParser):
    def __init__(__tmp1,
                 container_parser: ContainerParser,
                 __tmp2: <FILL>,
                 __tmp0: __typ0) -> None:
        __tmp1._parser_pipeline = ParserPipeline(container_parser)
        __tmp1._build_pipeline(__tmp2, __tmp0)
        super().__init__(container_parser,
                         __tmp1._parser_pipeline,
                         __tmp0)

    def _build_pipeline(__tmp1,
                        __tmp2: int,
                        __tmp0: __typ0) :
        partial_fill = partial(fill_empty, __tmp2=__tmp2)
        partial_filter = partial(filter_target,
                                 __tmp0=__tmp0)
        __tmp1._parser_pipeline.build([partial_fill, partial_filter])
