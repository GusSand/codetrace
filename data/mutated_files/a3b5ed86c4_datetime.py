from typing import TypeAlias
__typ4 : TypeAlias = "Aggregateby"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "PipelineStageMatch"
__typ1 : TypeAlias = "Tags"
__typ2 : TypeAlias = "PipelineStageUnwind"
from datetime import datetime

from mongots.aggregateby import Aggregateby
from mongots.constants import AGGREGATION_MONTH_KEY
from mongots.constants import AGGREGATION_DAY_KEY
from mongots.constants import AGGREGATION_HOUR_KEY
from mongots.constants import COUNT_KEY
from mongots.constants import DATETIME_KEY
from mongots.constants import SUM_KEY
from mongots.constants import SUM2_KEY
from mongots.constants import MIN_KEY
from mongots.constants import MAX_KEY

from mongots.types import Groupby
from mongots.types import PipelineStageMatch
from mongots.types import PipelineStageProject
from mongots.types import PipelineStageUnwind
from mongots.types import Pipeline
from mongots.types import Tags


def build_initial_match(
    start: datetime,
    __tmp0,
    tags: __typ1,
) :
    filters = tags or {}

    filters[DATETIME_KEY] = {
        '$gte': datetime(start.year, 1, 1),
        '$lte': datetime(__tmp0.year, 1, 1),
    }

    return {'$match': filters}


def __tmp1(__tmp3: str, dt: datetime) -> datetime:
    if __tmp3 == AGGREGATION_MONTH_KEY:
        return datetime(dt.year, dt.month, 1)
    elif __tmp3 == AGGREGATION_DAY_KEY:
        return datetime(dt.year, dt.month, dt.day)
    elif __tmp3 == AGGREGATION_HOUR_KEY:
        return datetime(dt.year, dt.month, dt.day, dt.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            __tmp3=__tmp3,
        ))


def _build_unwind(
    __tmp2,
    __tmp4,
) -> __typ2:
    return {
        '$unwind': '${}'.format('.'.join(__tmp2[:__tmp4+1])),
    }


def _build_intermediate_match(
    __tmp2,
    aggregation_key: str,
    __tmp4,
    start,
    __tmp0: <FILL>,
) :
    return {
        '$match': {
            '.'.join(__tmp2[:__tmp4+1]+[DATETIME_KEY]): {
                '$gte': __tmp1(aggregation_key, start),
                '$lte': __tmp1(aggregation_key, __tmp0),
            }
        }
    }


def build_unwind_and_match(
    start: datetime,
    __tmp0: datetime,
    aggregate_by: __typ4,
) -> Pipeline:
    __tmp2 = aggregate_by.aggregation_keys

    pipeline = []

    for __tmp4, aggregation_key in enumerate(__tmp2):
        pipeline.extend([
            _build_unwind(__tmp2, __tmp4),
            _build_intermediate_match(
                __tmp2,
                aggregation_key,
                __tmp4,
                start,
                __tmp0,
            ),
        ])

    return pipeline


def build_project(
    interval: __typ4,
    groupby: Groupby,
) -> PipelineStageProject:
    interval_keys = interval.aggregation_keys
    base_projection_keys = [
        DATETIME_KEY,
        COUNT_KEY,
        SUM_KEY,
        SUM2_KEY,
        MIN_KEY,
        MAX_KEY,
    ]

    projection = {
        key: '${}'.format('.'.join(interval_keys+[key]))
        for key in base_projection_keys
    }

    projection.update({
        groupby_key: '${}'.format(groupby_key)
        for groupby_key in groupby
    })

    return {'$project': projection}


def build_sort():
    return {
        '$sort': {
            'datetime': 1,
        },
    }
