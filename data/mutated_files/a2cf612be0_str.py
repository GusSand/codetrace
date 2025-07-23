from typing import TypeAlias
__typ1 : TypeAlias = "ContainerParser"
from functools import partial
from parser.container_parser import ContainerParser
from parser.face_vector_parser import FaceVectorParser
from parser.pipeline.parser_pipeline import ParserPipeline
from parser.pipeline.parser_pipeline_funcs import filter_target
from parser.pipeline.parser_pipeline_funcs import remove_empty


class __typ0(FaceVectorParser):
    def __init__(__tmp0,
                 container_parser,
                 __tmp1: <FILL>) :
        __tmp0._parser_pipeline = ParserPipeline(container_parser)
        __tmp0._build_pipeline(__tmp1)
        super().__init__(container_parser,
                         __tmp0._parser_pipeline,
                         __tmp1)

    def _build_pipeline(__tmp0, __tmp1) -> None:
        partial_filter = partial(filter_target,
                                 __tmp1=__tmp1)
        __tmp0._parser_pipeline.build([remove_empty, partial_filter])
