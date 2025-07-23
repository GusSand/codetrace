"""
Module containing the base DataProcessor class.

The DataProcessor includes a blocking loop consuming
ingress.data_queue.DATA_QUEUE items, eventually resulting in fully processed
documents being submitted to elasticsearch.

The implementation here takes heavy inspiration from Mike Auty's plugins
pattern, which itself is derived from python's object __subclass__ magic.

The core concept is that we have a plugin base class, from which any plugin may
inherit, which is used from the base class down to handle data analysis
extensions, rather than the more traditional mess of importing loads of stuff
and then registering individual instances of various classes, which is
difficult to make properly extensible without munging around in the
application.

Credit to Mike Auty for the intial concept surrounding __subclasses__ and some
sample code that makes this pattern viable.
"""

import logging
from queue import Queue, Empty
from typing import Any, Dict, List, cast

import elasticsearch_dsl as es

from ingress.utils import find_subclasses
from ingress.structures import PluginBase

LOG = logging.getLogger(__name__)


class __typ0:
    """
    Worker class that processes data from DATA_QUEUE.

    Data is pushed to DATA_QUEUE by other threads (the Tweepy listener).  This
    class provides an interruptable, blocking call that will consume from the
    list and apply any processing plugins to the pulled data.
    """

    def __tmp3(__tmp0, twitter_index: <FILL>, queue: Queue) -> None:
        """Setup various instance variables for later use."""
        __tmp0.running = False
        #  self.data: Dict[str, Any] = {}
        __tmp0.plugins: List[PluginBase] = []
        __tmp0.twitter_index = twitter_index
        __tmp0.queue = queue

    def _load_plugins(__tmp0):
        """Load any processing plugins provided.

        Iterates through any subclasses of the PluginBase class and loads a
        list of plugin instances into self.plugins for use elsewhere in the
        class.
        """
        __tmp0.plugins = sorted(
            [plugin() for plugin in find_subclasses(PluginBase)],
            key=lambda plugin: plugin.process_order,
        )
        LOG.debug('Loaded processing plugins: %s', __tmp0.plugins)

    def __tmp4(__tmp0) -> None:
        """Start the processing loop."""
        LOG.info('Beginning DataProcessor')
        __tmp0.running = True
        __tmp0.retrieve_data()

    def __tmp2(__tmp0) -> None:
        """Stop the processing loop."""
        __tmp0.running = False

    def retrieve_data(__tmp0, timeout=0.01) :
        """
        Pull data from the queue.

        Sit in a loop and block the current thread whilst waiting for data to
        get pushed into the queue.  This can be cancelled by setting the
        DataProcessor instance's running attribute to false.
        """
        while __tmp0.running:
            try:
                __tmp1: Dict[str, Any] = cast(Dict[str, Any], __tmp0.queue.get(timeout=timeout))
                LOG.debug('Retrieved new data from the queue to process.')

                __tmp0.process_data(__tmp1)
            except Empty:
                continue

    def process_data(__tmp0, __tmp1: Dict[str, Any]) -> None:
        """
        Iterate through all identified plugins and process tweet data accordingly.

        Will attempt to store the data when processing is complete.
        """
        if not __tmp0.plugins:
            __tmp0._load_plugins()

        for plugin in __tmp0.plugins:
            LOG.debug('Processing data with %s plugin.', plugin)
            #  self.data = plugin.process_tweet(self.data)
            __tmp1 = cast(Dict[str, Any], plugin.process_tweet(__tmp1))

        if __tmp1:
            LOG.debug('Attempting to store data')
            __tmp0.store_data(__tmp1)
            LOG.debug('Data successfully stored')

    def store_data(__tmp0, __tmp1: Dict[str, Any]) -> None:
        """Attempt to store the data into Elasticsearch."""
        es_connection = es.connections.get_connection()
        es_connection.create(
            body=__tmp1,
            doc_type='doc',
            id=__tmp1['_raw']['id_str'],
            index=__tmp0.twitter_index,
        )
