"""Stub module used to define the Celery class instance.

The Celery class instance is used when decorating celery tasks as well as when
launching a celery worker thread.  For this reason its advised to keep the
celery instance in a stand alone module, to help prevent circular imports.
"""

from typing import Dict, Any
from queue import Queue

from celery import Celery

from ingress import ES_CONNECTION_STRING
from ingress.utils import get_singleton_instance, create_es_connection
from ingress.structures import PluginBase
from ingress.data_processing.processing import DataProcessor


CELERY = Celery(
    'ingress',
    broker='amqp://rabbitmq:5672',
    results='redis://redis:6379',
)


create_es_connection(ES_CONNECTION_STRING)
PluginBase.import_subclasses()


@CELERY.task
def __tmp0(twitter_index: <FILL>, tweet_data):
    """Setup routine that preps a celery worker to run processing work.

    Ensures that all plugins have been imported and that a DataProcessor class
    has been instantiated and prepped ready to process tasks.
    """
    data_processor = get_singleton_instance(
        DataProcessor,
        twitter_index=twitter_index,
        queue=Queue()
    )
    # Currently the below command will run the data through all plugins and
    # then save it to the ES database.
    data_processor.process_data(tweet_data)

    # This is an arbitrary return, we could return data over celery from here
    # if needed.
    return True
