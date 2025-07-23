from typing import TypeAlias
__typ2 : TypeAlias = "Tags"
__typ5 : TypeAlias = "PipelineStageMatch"
__typ1 : TypeAlias = "int"
__typ3 : TypeAlias = "str"
__typ0 : TypeAlias = "PipelineStageProject"
__typ4 : TypeAlias = "PipelineStageUnwind"
__typ7 : TypeAlias = "Groupby"
__typ6 : TypeAlias = "Aggregateby"
__typ8 : TypeAlias = "Pipeline"
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
    start,
    end,
    tags,
) -> __typ5:
    filters = tags or {}

    filters[DATETIME_KEY] = {
        '$gte': datetime(start.year, 1, 1),
        '$lte': datetime(end.year, 1, 1),
    }

    return {'$match': filters}


def _get_floor_datetime(aggregation_level, dt: datetime) -> datetime:
    if aggregation_level == AGGREGATION_MONTH_KEY:
        return datetime(dt.year, dt.month, 1)
    elif aggregation_level == AGGREGATION_DAY_KEY:
        return datetime(dt.year, dt.month, dt.day)
    elif aggregation_level == AGGREGATION_HOUR_KEY:
        return datetime(dt.year, dt.month, dt.day, dt.hour)
    else:
        raise Exception('Bad aggregation_level {aggregation_level}'.format(
            aggregation_level=aggregation_level,
        ))


def __tmp1(
    aggregate_by_keys,
    __tmp0,
) -> __typ4:
    return {
        '$unwind': '${}'.format('.'.join(aggregate_by_keys[:__tmp0+1])),
    }


def __tmp2(
    aggregate_by_keys,
    aggregation_key: __typ3,
    __tmp0: __typ1,
    start: datetime,
    end: datetime,
) -> __typ5:
    return {
        '$match': {
            '.'.join(aggregate_by_keys[:__tmp0+1]+[DATETIME_KEY]): {
                '$gte': _get_floor_datetime(aggregation_key, start),
                '$lte': _get_floor_datetime(aggregation_key, end),
            }
        }
    }


def build_unwind_and_match(
    start: <FILL>,
    end: datetime,
    aggregate_by: __typ6,
) -> __typ8:
    aggregate_by_keys = aggregate_by.aggregation_keys

    pipeline = []

    for __tmp0, aggregation_key in enumerate(aggregate_by_keys):
        pipeline.extend([
            __tmp1(aggregate_by_keys, __tmp0),
            __tmp2(
                aggregate_by_keys,
                aggregation_key,
                __tmp0,
                start,
                end,
            ),
        ])

    return pipeline


def build_project(
    interval,
    groupby,
) -> __typ0:
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
