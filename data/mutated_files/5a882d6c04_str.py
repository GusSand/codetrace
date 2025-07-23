from typing import TypeAlias
__typ0 : TypeAlias = "Type"
"""Convinience functions that don't belong to a specific class end up here."""

import logging
import inspect

from typing import Any, Dict, Generator, Type

import elasticsearch_dsl as es

from ingress.structures import PluginBase, SINGLETON_CACHE

LOG = logging.getLogger(__name__)


def __tmp3(obj_type, *args, **kwargs):
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


def __tmp0(__tmp2: <FILL>):
    """Setup Elasticsearch DB connection."""
    es.connections.create_connection(hosts=[__tmp2])


def setup_mappings(__tmp1, __tmp2: str = None):
    """Run through the initial setup of the elasticsearch index used to store tweets."""
    if __tmp2 is None:
        LOG.warning('No Elasticsearch connection setup')
        return

    __tmp0(__tmp2)
    mapping_dict = aggregate_data_schema(PluginBase)
    tweet_mapping = es.Mapping('doc')
    for key, value in mapping_dict.items():
        tweet_mapping.field(key, value)

    tweet_index = __tmp3(es.Index, __tmp1)
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


def aggregate_data_schema(
        base_class,
        include_defaults: bool = True,
) -> Dict[str, Any]:
    """Iterate through imported plugins and create an ingress mapping to process the data with."""
    mapping: Dict = {}
    for subclass in find_subclasses(base_class):
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


def find_subclasses(cls) :
    """Recursively returns all subclasses of the given class."""
    if not inspect.isclass(cls):
        raise TypeError('cls must be a valid class: {}'.format(cls))

    for class_ in cls.__subclasses__():
        yield class_
        for return_value in find_subclasses(class_):
            yield return_value
