from typing import TypeAlias
__typ0 : TypeAlias = "Pipeline"
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
    start: datetime,
    __tmp1,
    tags,
) :
    filters = tags or {}

    filters[DATETIME_KEY] = {
        '$gte': datetime(start.year, 1, 1),
        '$lte': datetime(__tmp1.year, 1, 1),
    }

    return {'$match': filters}


def _get_floor_datetime(aggregation_level, dt) :
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


def _build_unwind(
    aggregate_by_keys,
    end_index: int,
) :
    return {
        '$unwind': '${}'.format('.'.join(aggregate_by_keys[:end_index+1])),
    }


def _build_intermediate_match(
    aggregate_by_keys,
    aggregation_key: str,
    end_index,
    start: <FILL>,
    __tmp1: datetime,
) :
    return {
        '$match': {
            '.'.join(aggregate_by_keys[:end_index+1]+[DATETIME_KEY]): {
                '$gte': _get_floor_datetime(aggregation_key, start),
                '$lte': _get_floor_datetime(aggregation_key, __tmp1),
            }
        }
    }


def build_unwind_and_match(
    start,
    __tmp1,
    aggregate_by: Aggregateby,
) :
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
    __tmp0,
    groupby,
) -> PipelineStageProject:
    interval_keys = __tmp0.aggregation_keys
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


def __tmp2():
    return {
        '$sort': {
            'datetime': 1,
        },
    }
