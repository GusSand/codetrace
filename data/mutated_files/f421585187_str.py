from typing import TypeAlias
__typ0 : TypeAlias = "Type"
"""Convinience functions that don't belong to a specific class end up here."""

import logging
import inspect

from typing import Any, Dict, Generator, Type

import elasticsearch_dsl as es

from ingress.structures import PluginBase, SINGLETON_CACHE

LOG = logging.getLogger(__name__)


def get_singleton_instance(obj_type, *args, **kwargs):
    """Factory that produces a cached class instances."""
    LOG.debug('Attempting to retrieve cached %s', obj_type)
    if obj_type not in SINGLETON_CACHE:
        LOG.debug('%s not found, instantiating new instance', obj_type)
        object_instance = obj_type(*args, **kwargs)
        SINGLETON_CACHE[obj_type] = object_instance
    else:
        LOG.debug('%s found, returning cached instance', obj_type)
        object_instance = SINGLETON_CACHE[obj_type]

    return object_instance


def create_es_connection(__tmp4):
    """Setup Elasticsearch DB connection."""
    es.connections.create_connection(hosts=[__tmp4])


def __tmp2(__tmp0: <FILL>, __tmp4: str = None):
    """Run through the initial setup of the elasticsearch index used to store tweets."""
    if __tmp4 is None:
        LOG.warning('No Elasticsearch connection setup')
        return

    create_es_connection(__tmp4)
    mapping_dict = __tmp1(PluginBase)
    tweet_mapping = es.Mapping('doc')
    for key, value in mapping_dict.items():
        tweet_mapping.field(key, value)

    tweet_index = get_singleton_instance(es.Index, __tmp0)
    LOG.info('Storing tweets in %s', __tmp0)
    tweet_index.settings(
        **{
            "index.mapping.total_fields.limit": 5000,
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
    )
    #  tweet_index.document(Tweet)
    tweet_index.mapping(tweet_mapping)
    LOG.info('Checking if Index %s exists and creating if not', __tmp0)
    if not tweet_index.exists():
        LOG.info('Creating new index.')
        tweet_index.create()
    else:
        LOG.info('Index exists, ensuring its up to date.')
        tweet_index.save()


def __tmp1(
        __tmp3: __typ0,
        include_defaults: bool = True,
) -> Dict[str, Any]:
    """Iterate through imported plugins and create an ingress mapping to process the data with."""
    mapping: Dict = {}
    for subclass in __tmp5(__tmp3):
        subclass_data_schema = None
        try:
            subclass_data_schema = getattr(subclass, 'data_schema')
        except AttributeError:
            continue
        if subclass_data_schema:
            mapping.update(subclass_data_schema)

    if include_defaults:
        mapping['_raw'] = es.Object(dynamic=True)
        mapping['timestamp'] = es.Date()

    return mapping


def __tmp5(cls: __typ0) -> Generator[__typ0, None, None]:
    """Recursively returns all subclasses of the given class."""
    if not inspect.isclass(cls):
        raise TypeError('cls must be a valid class: {}'.format(cls))

    for class_ in cls.__subclasses__():
        yield class_
        for return_value in __tmp5(class_):
            yield return_value
