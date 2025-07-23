from typing import TypeAlias
__typ1 : TypeAlias = "PipelineStageUnwind"
__typ0 : TypeAlias = "int"
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


def __tmp7(
    __tmp8: datetime,
    __tmp1: <FILL>,
    __tmp6,
) -> PipelineStageMatch:
    filters = __tmp6 or {}

    filters[DATETIME_KEY] = {
        '$gte': datetime(__tmp8.year, 1, 1),
        '$lte': datetime(__tmp1.year, 1, 1),
    }

    return {'$match': filters}


def _get_floor_datetime(aggregation_level: str, __tmp0) :
    if aggregation_level == AGGREGATION_MONTH_KEY:
        return datetime(__tmp0.year, __tmp0.month, 1)
    elif aggregation_level == AGGREGATION_DAY_KEY:
        return datetime(__tmp0.year, __tmp0.month, __tmp0.day)
    elif aggregation_level == AGGREGATION_HOUR_KEY:
        return datetime(__tmp0.year, __tmp0.month, __tmp0.day, __tmp0.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            aggregation_level=aggregation_level,
        ))


def __tmp5(
    __tmp3,
    end_index,
) :
    return {
        '$unwind': '${}'.format('.'.join(__tmp3[:end_index+1])),
    }


def _build_intermediate_match(
    __tmp3,
    aggregation_key: str,
    end_index,
    __tmp8: datetime,
    __tmp1: datetime,
) -> PipelineStageMatch:
    return {
        '$match': {
            '.'.join(__tmp3[:end_index+1]+[DATETIME_KEY]): {
                '$gte': _get_floor_datetime(aggregation_key, __tmp8),
                '$lte': _get_floor_datetime(aggregation_key, __tmp1),
            }
        }
    }


def build_unwind_and_match(
    __tmp8: datetime,
    __tmp1: datetime,
    aggregate_by: Aggregateby,
) -> Pipeline:
    __tmp3 = aggregate_by.aggregation_keys

    pipeline = []

    for end_index, aggregation_key in enumerate(__tmp3):
        pipeline.extend([
            __tmp5(__tmp3, end_index),
            _build_intermediate_match(
                __tmp3,
                aggregation_key,
                end_index,
                __tmp8,
                __tmp1,
            ),
        ])

    return pipeline


def __tmp2(
    __tmp4: Aggregateby,
    groupby,
) -> PipelineStageProject:
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
        for groupby_key in groupby
    })

    return {'$project': projection}


def build_sort():
    return {
        '$sort': {
            'datetime': 1,
        },
    }
