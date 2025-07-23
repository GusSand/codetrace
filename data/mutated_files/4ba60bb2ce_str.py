from typing import TypeAlias
__typ1 : TypeAlias = "FaceVectorMetric"
__typ2 : TypeAlias = "ContainerParser"
from parser.container_parser import ContainerParser
from parser.pair import Pair
from parser.parser_base import ParserBase
from parser.pipeline.parser_pipeline import ParserPipeline
from typing import Iterable

from metrics.metrics import FaceVectorMetric


class __typ0(ParserBase):

    def __init__(__tmp0,
                 container_parser,
                 parser_pipeline,
                 distance_metric: <FILL>) -> None:
        __tmp0._container_parser = container_parser
        __tmp0._distance_metric = distance_metric
        __tmp0._parser_pipeline = parser_pipeline

    def compute_pairs(__tmp0) :
        return __tmp0._parser_pipeline.execute_pipeline()

    def compute_metrics(__tmp0) -> __typ1:
        pairs = list(__tmp0._container_parser.compute_pairs())
        num_expected = len(pairs)
        num_existing = sum(1 for pair in pairs if pair.image1 and pair.image2)
        num_missing = num_expected - num_existing
        percentage_missing = 100 * (num_missing / num_expected)
        return __typ1(num_expected, num_missing, percentage_missing)
