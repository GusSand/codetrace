from typing import TypeAlias
__typ4 : TypeAlias = "PipelineStageMatch"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "PipelineStageUnwind"
__typ5 : TypeAlias = "Aggregateby"
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "Tags"
__typ6 : TypeAlias = "Groupby"
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


def __tmp6(
    start,
    __tmp0,
    __tmp4,
) :
    filters = __tmp4 or {}

    filters[DATETIME_KEY] = {
        '$gte': datetime(start.year, 1, 1),
        '$lte': datetime(__tmp0.year, 1, 1),
    }

    return {'$match': filters}


def _get_floor_datetime(__tmp2, dt: datetime) :
    if __tmp2 == AGGREGATION_MONTH_KEY:
        return datetime(dt.year, dt.month, 1)
    elif __tmp2 == AGGREGATION_DAY_KEY:
        return datetime(dt.year, dt.month, dt.day)
    elif __tmp2 == AGGREGATION_HOUR_KEY:
        return datetime(dt.year, dt.month, dt.day, dt.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            __tmp2=__tmp2,
        ))


def __tmp3(
    aggregate_by_keys,
    __tmp8: __typ0,
) :
    return {
        '$unwind': '${}'.format('.'.join(aggregate_by_keys[:__tmp8+1])),
    }


def _build_intermediate_match(
    aggregate_by_keys,
    __tmp5,
    __tmp8: __typ0,
    start,
    __tmp0,
) :
    return {
        '$match': {
            '.'.join(aggregate_by_keys[:__tmp8+1]+[DATETIME_KEY]): {
                '$gte': _get_floor_datetime(__tmp5, start),
                '$lte': _get_floor_datetime(__tmp5, __tmp0),
            }
        }
    }


def build_unwind_and_match(
    start: datetime,
    __tmp0: <FILL>,
    aggregate_by,
) -> Pipeline:
    aggregate_by_keys = aggregate_by.aggregation_keys

    pipeline = []

    for __tmp8, __tmp5 in enumerate(aggregate_by_keys):
        pipeline.extend([
            __tmp3(aggregate_by_keys, __tmp8),
            _build_intermediate_match(
                aggregate_by_keys,
                __tmp5,
                __tmp8,
                start,
                __tmp0,
            ),
        ])

    return pipeline


def build_project(
    __tmp1,
    __tmp7: __typ6,
) :
    interval_keys = __tmp1.aggregation_keys
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
        for groupby_key in __tmp7
    })

    return {'$project': projection}


def build_sort():
    return {
        '$sort': {
            'datetime': 1,
        },
    }
