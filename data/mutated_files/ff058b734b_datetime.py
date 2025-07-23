from typing import TypeAlias
__typ4 : TypeAlias = "PipelineStageMatch"
__typ2 : TypeAlias = "Tags"
__typ1 : TypeAlias = "int"
__typ7 : TypeAlias = "Pipeline"
__typ5 : TypeAlias = "Aggregateby"
__typ3 : TypeAlias = "str"
__typ0 : TypeAlias = "PipelineStageProject"
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


def __tmp9(
    __tmp12,
    __tmp0,
    __tmp7: __typ2,
) -> __typ4:
    filters = __tmp7 or {}

    filters[DATETIME_KEY] = {
        '$gte': datetime(__tmp12.year, 1, 1),
        '$lte': datetime(__tmp0.year, 1, 1),
    }

    return {'$match': filters}


def __tmp2(__tmp5, dt: <FILL>) :
    if __tmp5 == AGGREGATION_MONTH_KEY:
        return datetime(dt.year, dt.month, 1)
    elif __tmp5 == AGGREGATION_DAY_KEY:
        return datetime(dt.year, dt.month, dt.day)
    elif __tmp5 == AGGREGATION_HOUR_KEY:
        return datetime(dt.year, dt.month, dt.day, dt.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            __tmp5=__tmp5,
        ))


def __tmp6(
    __tmp3,
    end_index: __typ1,
) -> PipelineStageUnwind:
    return {
        '$unwind': '${}'.format('.'.join(__tmp3[:end_index+1])),
    }


def __tmp13(
    __tmp3,
    __tmp8,
    end_index,
    __tmp12: datetime,
    __tmp0,
) -> __typ4:
    return {
        '$match': {
            '.'.join(__tmp3[:end_index+1]+[DATETIME_KEY]): {
                '$gte': __tmp2(__tmp8, __tmp12),
                '$lte': __tmp2(__tmp8, __tmp0),
            }
        }
    }


def __tmp10(
    __tmp12,
    __tmp0,
    aggregate_by,
) :
    __tmp3 = aggregate_by.aggregation_keys

    pipeline = []

    for end_index, __tmp8 in enumerate(__tmp3):
        pipeline.extend([
            __tmp6(__tmp3, end_index),
            __tmp13(
                __tmp3,
                __tmp8,
                end_index,
                __tmp12,
                __tmp0,
            ),
        ])

    return pipeline


def __tmp1(
    __tmp4: __typ5,
    __tmp11,
) :
    interval_keys = __tmp4.aggregation_keys
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
        for groupby_key in __tmp11
    })

    return {'$project': projection}


def build_sort():
    return {
        '$sort': {
            'datetime': 1,
        },
    }
