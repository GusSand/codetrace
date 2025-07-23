from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"
from datetime import datetime
from pymongo.collection import Collection

from mongots.types import MetadataTags
from mongots.types import MetadataTimeRange
from mongots.types import Tags


class __typ1():
    def __init__(
        __tmp1,
        metadata_collection,
    ) :
        __tmp1._metadata_collection = metadata_collection

    def update(
        __tmp1,
        __tmp0,
        timestamp: <FILL>,
        tags: Tags = None,
    ) :

        update_query = {
            '$inc': {'count': 1},
            '$min': {'timerange.min': timestamp},
            '$max': {'timerange.max': timestamp},
        }

        if tags is not None and tags != {}:
            update_query['$addToSet'] = {
                'tags.{}'.format(tag): tags[tag]
                for tag in tags
            }

        result = __tmp1._metadata_collection.update_one({
            'collection_name': __tmp0,
        }, update_query, upsert=True)

        return result.acknowledged \
            and (1 == result.matched_count or result.upserted_id is not None)

    def get_tags(
        __tmp1,
        __tmp0,
    ) :

        mongo_tags = __tmp1._metadata_collection.find_one({
            'collection_name': __tmp0,
        }, {
            'tags': 1,
        }) or {}

        return mongo_tags.get('tags', {})

    def get_timerange(
        __tmp1,
        __tmp0,
    ) :

        mongo_timerange = __tmp1._metadata_collection.find_one({
            'collection_name': __tmp0,
        }, {
            'timerange': 1,
        })

        if mongo_timerange is None:
            return None

        return (
            mongo_timerange['timerange']['min'],
            mongo_timerange['timerange']['max'],
        )

    def _format_collection(__tmp1, collection):
        return {
            'collection_name': collection['collection_name'],
            'count': collection.get('count', 0),
            'tags': collection.get('tags', {}),
            'timerange': (
                collection['timerange']['min'],
                collection['timerange']['max'],
            ),
        }

    def get_collections(__tmp1):
        return [
            __tmp1._format_collection(collection)
            for collection in __tmp1._metadata_collection.find({}, {'_id': 0})
        ]
