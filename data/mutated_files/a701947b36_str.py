from typing import TypeAlias
__typ5 : TypeAlias = "Groupby"
__typ4 : TypeAlias = "Aggregateby"
__typ6 : TypeAlias = "Pipeline"
__typ3 : TypeAlias = "PipelineStageMatch"
__typ0 : TypeAlias = "PipelineStageProject"
__typ1 : TypeAlias = "datetime"
__typ2 : TypeAlias = "int"
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
    __tmp13,
    __tmp2: __typ1,
    __tmp9: Tags,
) -> __typ3:
    filters = __tmp9 or {}

    filters[DATETIME_KEY] = {
        '$gte': __typ1(__tmp13.year, 1, 1),
        '$lte': __typ1(__tmp2.year, 1, 1),
    }

    return {'$match': filters}


def __tmp4(__tmp8, __tmp1: __typ1) :
    if __tmp8 == AGGREGATION_MONTH_KEY:
        return __typ1(__tmp1.year, __tmp1.month, 1)
    elif __tmp8 == AGGREGATION_DAY_KEY:
        return __typ1(__tmp1.year, __tmp1.month, __tmp1.day)
    elif __tmp8 == AGGREGATION_HOUR_KEY:
        return __typ1(__tmp1.year, __tmp1.month, __tmp1.day, __tmp1.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            __tmp8=__tmp8,
        ))


def _build_unwind(
    __tmp5,
    __tmp6,
) :
    return {
        '$unwind': '${}'.format('.'.join(__tmp5[:__tmp6+1])),
    }


def __tmp14(
    __tmp5,
    aggregation_key: <FILL>,
    __tmp6: __typ2,
    __tmp13,
    __tmp2,
) -> __typ3:
    return {
        '$match': {
            '.'.join(__tmp5[:__tmp6+1]+[DATETIME_KEY]): {
                '$gte': __tmp4(aggregation_key, __tmp13),
                '$lte': __tmp4(aggregation_key, __tmp2),
            }
        }
    }


def __tmp10(
    __tmp13: __typ1,
    __tmp2,
    __tmp0,
) -> __typ6:
    __tmp5 = __tmp0.aggregation_keys

    pipeline = []

    for __tmp6, aggregation_key in enumerate(__tmp5):
        pipeline.extend([
            _build_unwind(__tmp5, __tmp6),
            __tmp14(
                __tmp5,
                aggregation_key,
                __tmp6,
                __tmp13,
                __tmp2,
            ),
        ])

    return pipeline


def __tmp3(
    __tmp7,
    groupby: __typ5,
) -> __typ0:
    interval_keys = __tmp7.aggregation_keys
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


def __tmp12():
    return {
        '$sort': {
            'datetime': 1,
        },
    }
