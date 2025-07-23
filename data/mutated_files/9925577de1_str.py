from typing import TypeAlias
__typ0 : TypeAlias = "MetadataTags"
__typ1 : TypeAlias = "MetadataTimeRange"
__typ3 : TypeAlias = "bool"
from datetime import datetime
from pymongo.collection import Collection

from mongots.types import MetadataTags
from mongots.types import MetadataTimeRange
from mongots.types import Tags


class __typ2():
    def __tmp5(
        __tmp0,
        __tmp4: Collection,
    ) -> None:
        __tmp0._metadata_collection = __tmp4

    def __tmp8(
        __tmp0,
        __tmp1: str,
        __tmp3,
        tags: Tags = None,
    ) -> __typ3:

        update_query = {
            '$inc': {'count': 1},
            '$min': {'timerange.min': __tmp3},
            '$max': {'timerange.max': __tmp3},
        }

        if tags is not None and tags != {}:
            update_query['$addToSet'] = {
                'tags.{}'.format(tag): tags[tag]
                for tag in tags
            }

        result = __tmp0._metadata_collection.update_one({
            'collection_name': __tmp1,
        }, update_query, upsert=True)

        return result.acknowledged \
            and (1 == result.matched_count or result.upserted_id is not None)

    def __tmp2(
        __tmp0,
        __tmp1: <FILL>,
    ) -> __typ0:

        mongo_tags = __tmp0._metadata_collection.find_one({
            'collection_name': __tmp1,
        }, {
            'tags': 1,
        }) or {}

        return mongo_tags.get('tags', {})

    def __tmp6(
        __tmp0,
        __tmp1,
    ) -> __typ1:

        mongo_timerange = __tmp0._metadata_collection.find_one({
            'collection_name': __tmp1,
        }, {
            'timerange': 1,
        })

        if mongo_timerange is None:
            return None

        return (
            mongo_timerange['timerange']['min'],
            mongo_timerange['timerange']['max'],
        )

    def _format_collection(__tmp0, collection):
        return {
            'collection_name': collection['collection_name'],
            'count': collection.get('count', 0),
            'tags': collection.get('tags', {}),
            'timerange': (
                collection['timerange']['min'],
                collection['timerange']['max'],
            ),
        }

    def __tmp7(__tmp0):
        return [
            __tmp0._format_collection(collection)
            for collection in __tmp0._metadata_collection.find({}, {'_id': 0})
        ]
