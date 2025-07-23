from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Convinience functions that don't belong to a specific class end up here."""

import logging
import inspect

from typing import Any, Dict, Generator, Type

import elasticsearch_dsl as es

from ingress.structures import PluginBase, SINGLETON_CACHE

LOG = logging.getLogger(__name__)


def __tmp7(__tmp0, *args, **kwargs):
    """Factory that produces a cached class instances."""
    LOG.debug('Attempting to retrieve cached %s', __tmp0)
    if __tmp0 not in SINGLETON_CACHE:
        LOG.debug('%s not found, instantiating new instance', __tmp0)
        object_instance = __tmp0(*args, **kwargs)
        SINGLETON_CACHE[__tmp0] = object_instance
    else:
        LOG.debug('%s found, returning cached instance', __tmp0)
        object_instance = SINGLETON_CACHE[__tmp0]

    return object_instance


def create_es_connection(__tmp5):
    """Setup Elasticsearch DB connection."""
    es.connections.create_connection(hosts=[__tmp5])


def __tmp3(__tmp1: __typ0, __tmp5: __typ0 = None):
    """Run through the initial setup of the elasticsearch index used to store tweets."""
    if __tmp5 is None:
        LOG.warning('No Elasticsearch connection setup')
        return

    create_es_connection(__tmp5)
    mapping_dict = __tmp2(PluginBase)
    tweet_mapping = es.Mapping('doc')
    for key, value in mapping_dict.items():
        tweet_mapping.field(key, value)

    tweet_index = __tmp7(es.Index, __tmp1)
    LOG.info('Storing tweets in %s', __tmp1)
    tweet_index.settings(
        **{
            "index.mapping.total_fields.limit": 5000,
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
    )
    #  tweet_index.document(Tweet)
    tweet_index.mapping(tweet_mapping)
    LOG.info('Checking if Index %s exists and creating if not', __tmp1)
    if not tweet_index.exists():
        LOG.info('Creating new index.')
        tweet_index.create()
    else:
        LOG.info('Index exists, ensuring its up to date.')
        tweet_index.save()


def __tmp2(
        __tmp4: Type,
        include_defaults: bool = True,
) :
    """Iterate through imported plugins and create an ingress mapping to process the data with."""
    mapping: Dict = {}
    for subclass in __tmp6(__tmp4):
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


def __tmp6(cls: <FILL>) :
    """Recursively returns all subclasses of the given class."""
    if not inspect.isclass(cls):
        raise TypeError('cls must be a valid class: {}'.format(cls))

    for class_ in cls.__subclasses__():
        yield class_
        for return_value in __tmp6(class_):
            yield return_value
