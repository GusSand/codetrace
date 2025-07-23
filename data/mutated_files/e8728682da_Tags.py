from typing import TypeAlias
__typ4 : TypeAlias = "PipelineStageMatch"
__typ1 : TypeAlias = "int"
__typ7 : TypeAlias = "Pipeline"
__typ3 : TypeAlias = "PipelineStageUnwind"
__typ5 : TypeAlias = "Aggregateby"
__typ2 : TypeAlias = "str"
__typ6 : TypeAlias = "Groupby"
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


def __tmp11(
    __tmp13: __typ0,
    __tmp2: __typ0,
    __tmp9: <FILL>,
) :
    filters = __tmp9 or {}

    filters[DATETIME_KEY] = {
        '$gte': __typ0(__tmp13.year, 1, 1),
        '$lte': __typ0(__tmp2.year, 1, 1),
    }

    return {'$match': filters}


def _get_floor_datetime(__tmp7: __typ2, __tmp1: __typ0) :
    if __tmp7 == AGGREGATION_MONTH_KEY:
        return __typ0(__tmp1.year, __tmp1.month, 1)
    elif __tmp7 == AGGREGATION_DAY_KEY:
        return __typ0(__tmp1.year, __tmp1.month, __tmp1.day)
    elif __tmp7 == AGGREGATION_HOUR_KEY:
        return __typ0(__tmp1.year, __tmp1.month, __tmp1.day, __tmp1.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            __tmp7=__tmp7,
        ))


def __tmp6(
    __tmp5,
    __tmp14: __typ1,
) :
    return {
        '$unwind': '${}'.format('.'.join(__tmp5[:__tmp14+1])),
    }


def __tmp3(
    __tmp5,
    __tmp10: __typ2,
    __tmp14: __typ1,
    __tmp13,
    __tmp2,
) -> __typ4:
    return {
        '$match': {
            '.'.join(__tmp5[:__tmp14+1]+[DATETIME_KEY]): {
                '$gte': _get_floor_datetime(__tmp10, __tmp13),
                '$lte': _get_floor_datetime(__tmp10, __tmp2),
            }
        }
    }


def build_unwind_and_match(
    __tmp13,
    __tmp2: __typ0,
    __tmp0: __typ5,
) :
    __tmp5 = __tmp0.aggregation_keys

    pipeline = []

    for __tmp14, __tmp10 in enumerate(__tmp5):
        pipeline.extend([
            __tmp6(__tmp5, __tmp14),
            __tmp3(
                __tmp5,
                __tmp10,
                __tmp14,
                __tmp13,
                __tmp2,
            ),
        ])

    return pipeline


def __tmp4(
    __tmp8: __typ5,
    __tmp12: __typ6,
) :
    interval_keys = __tmp8.aggregation_keys
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
        for groupby_key in __tmp12
    })

    return {'$project': projection}


def build_sort():
    return {
        '$sort': {
            'datetime': 1,
        },
    }
