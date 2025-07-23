from typing import TypeAlias
__typ2 : TypeAlias = "Tags"
__typ5 : TypeAlias = "PipelineStageMatch"
__typ7 : TypeAlias = "Pipeline"
__typ3 : TypeAlias = "str"
__typ1 : TypeAlias = "datetime"
__typ0 : TypeAlias = "PipelineStageProject"
__typ4 : TypeAlias = "PipelineStageUnwind"
__typ6 : TypeAlias = "Aggregateby"
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


def __tmp4(
    start,
    end,
    tags,
) :
    filters = tags or {}

    filters[DATETIME_KEY] = {
        '$gte': __typ1(start.year, 1, 1),
        '$lte': __typ1(end.year, 1, 1),
    }

    return {'$match': filters}


def __tmp0(aggregation_level: __typ3, dt) :
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


def __tmp1(
    aggregate_by_keys,
    __tmp6: <FILL>,
) :
    return {
        '$unwind': '${}'.format('.'.join(aggregate_by_keys[:__tmp6+1])),
    }


def _build_intermediate_match(
    aggregate_by_keys,
    __tmp3,
    __tmp6,
    start,
    end,
) :
    return {
        '$match': {
            '.'.join(aggregate_by_keys[:__tmp6+1]+[DATETIME_KEY]): {
                '$gte': __tmp0(__tmp3, start),
                '$lte': __tmp0(__tmp3, end),
            }
        }
    }


def build_unwind_and_match(
    start,
    end,
    aggregate_by,
) -> __typ7:
    aggregate_by_keys = aggregate_by.aggregation_keys

    pipeline = []

    for __tmp6, __tmp3 in enumerate(aggregate_by_keys):
        pipeline.extend([
            __tmp1(aggregate_by_keys, __tmp6),
            _build_intermediate_match(
                aggregate_by_keys,
                __tmp3,
                __tmp6,
                start,
                end,
            ),
        ])

    return pipeline


def __tmp5(
    __tmp2,
    groupby,
) :
    interval_keys = __tmp2.aggregation_keys
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
