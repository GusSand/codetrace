from typing import TypeAlias
__typ2 : TypeAlias = "Aggregateby"
__typ4 : TypeAlias = "Pipeline"
__typ1 : TypeAlias = "datetime"
__typ0 : TypeAlias = "PipelineStageProject"
__typ3 : TypeAlias = "Groupby"
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


def __tmp9(
    __tmp10,
    __tmp1,
    __tmp7,
) :
    filters = __tmp7 or {}

    filters[DATETIME_KEY] = {
        '$gte': __typ1(__tmp10.year, 1, 1),
        '$lte': __typ1(__tmp1.year, 1, 1),
    }

    return {'$match': filters}


def __tmp3(aggregation_level, dt) :
    if aggregation_level == AGGREGATION_MONTH_KEY:
        return __typ1(dt.year, dt.month, 1)
    elif aggregation_level == AGGREGATION_DAY_KEY:
        return __typ1(dt.year, dt.month, dt.day)
    elif aggregation_level == AGGREGATION_HOUR_KEY:
        return __typ1(dt.year, dt.month, dt.day, dt.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            aggregation_level=aggregation_level,
        ))


def __tmp5(
    __tmp4,
    end_index,
) :
    return {
        '$unwind': '${}'.format('.'.join(__tmp4[:end_index+1])),
    }


def _build_intermediate_match(
    __tmp4,
    __tmp8,
    end_index: <FILL>,
    __tmp10,
    __tmp1,
) -> PipelineStageMatch:
    return {
        '$match': {
            '.'.join(__tmp4[:end_index+1]+[DATETIME_KEY]): {
                '$gte': __tmp3(__tmp8, __tmp10),
                '$lte': __tmp3(__tmp8, __tmp1),
            }
        }
    }


def build_unwind_and_match(
    __tmp10,
    __tmp1: __typ1,
    __tmp0,
) :
    __tmp4 = __tmp0.aggregation_keys

    pipeline = []

    for end_index, __tmp8 in enumerate(__tmp4):
        pipeline.extend([
            __tmp5(__tmp4, end_index),
            _build_intermediate_match(
                __tmp4,
                __tmp8,
                end_index,
                __tmp10,
                __tmp1,
            ),
        ])

    return pipeline


def __tmp2(
    __tmp6,
    groupby,
) :
    interval_keys = __tmp6.aggregation_keys
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
