from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ4 : TypeAlias = "Pipeline"
__typ1 : TypeAlias = "str"
__typ3 : TypeAlias = "Aggregateby"
__typ2 : TypeAlias = "PipelineStageMatch"
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
    start: <FILL>,
    __tmp1: datetime,
    tags,
) -> __typ2:
    filters = tags or {}

    filters[DATETIME_KEY] = {
        '$gte': datetime(start.year, 1, 1),
        '$lte': datetime(__tmp1.year, 1, 1),
    }

    return {'$match': filters}


def __tmp0(__tmp2: __typ1, dt: datetime) -> datetime:
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


def _build_unwind(
    aggregate_by_keys,
    end_index: __typ0,
) -> PipelineStageUnwind:
    return {
        '$unwind': '${}'.format('.'.join(aggregate_by_keys[:end_index+1])),
    }


def _build_intermediate_match(
    aggregate_by_keys,
    aggregation_key: __typ1,
    end_index: __typ0,
    start: datetime,
    __tmp1: datetime,
) -> __typ2:
    return {
        '$match': {
            '.'.join(aggregate_by_keys[:end_index+1]+[DATETIME_KEY]): {
                '$gte': __tmp0(aggregation_key, start),
                '$lte': __tmp0(aggregation_key, __tmp1),
            }
        }
    }


def build_unwind_and_match(
    start: datetime,
    __tmp1: datetime,
    aggregate_by: __typ3,
) -> __typ4:
    aggregate_by_keys = aggregate_by.aggregation_keys

    pipeline = []

    for end_index, aggregation_key in enumerate(aggregate_by_keys):
        pipeline.extend([
            _build_unwind(aggregate_by_keys, end_index),
            _build_intermediate_match(
                aggregate_by_keys,
                aggregation_key,
                end_index,
                start,
                __tmp1,
            ),
        ])

    return pipeline


def build_project(
    interval: __typ3,
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
