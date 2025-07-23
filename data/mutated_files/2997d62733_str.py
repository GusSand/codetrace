from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
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
    __tmp7: __typ0,
    end,
    __tmp5,
) -> PipelineStageMatch:
    filters = __tmp5 or {}

    filters[DATETIME_KEY] = {
        '$gte': __typ0(__tmp7.year, 1, 1),
        '$lte': __typ0(end.year, 1, 1),
    }

    return {'$match': filters}


def _get_floor_datetime(aggregation_level: <FILL>, __tmp1: __typ0) :
    if aggregation_level == AGGREGATION_MONTH_KEY:
        return __typ0(__tmp1.year, __tmp1.month, 1)
    elif aggregation_level == AGGREGATION_DAY_KEY:
        return __typ0(__tmp1.year, __tmp1.month, __tmp1.day)
    elif aggregation_level == AGGREGATION_HOUR_KEY:
        return __typ0(__tmp1.year, __tmp1.month, __tmp1.day, __tmp1.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            aggregation_level=aggregation_level,
        ))


def __tmp4(
    aggregate_by_keys,
    __tmp8: int,
) -> PipelineStageUnwind:
    return {
        '$unwind': '${}'.format('.'.join(aggregate_by_keys[:__tmp8+1])),
    }


def __tmp2(
    aggregate_by_keys,
    __tmp6: str,
    __tmp8,
    __tmp7,
    end,
) :
    return {
        '$match': {
            '.'.join(aggregate_by_keys[:__tmp8+1]+[DATETIME_KEY]): {
                '$gte': _get_floor_datetime(__tmp6, __tmp7),
                '$lte': _get_floor_datetime(__tmp6, end),
            }
        }
    }


def build_unwind_and_match(
    __tmp7,
    end,
    __tmp0,
) :
    aggregate_by_keys = __tmp0.aggregation_keys

    pipeline = []

    for __tmp8, __tmp6 in enumerate(aggregate_by_keys):
        pipeline.extend([
            __tmp4(aggregate_by_keys, __tmp8),
            __tmp2(
                aggregate_by_keys,
                __tmp6,
                __tmp8,
                __tmp7,
                end,
            ),
        ])

    return pipeline


def build_project(
    __tmp3: Aggregateby,
    groupby,
) :
    interval_keys = __tmp3.aggregation_keys
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
