import json


class CollectionClient:
    """ Client used for all the operations that can be done to collections.
    """
    def __init__(__tmp0, session):
        __tmp0.session = session

    def collections(__tmp0, query: dict = None):
        """ Gets list of the collections.
        """
        return __tmp0.session.get('/v4/collections/', params=query or {})

    def __tmp4(__tmp0, __tmp7):
        """ Gets all the collection information for a specific collection id.
        """
        return __tmp0.session.get(f'/v4/collections/{__tmp7}/')

    def create_collection(__tmp0, __tmp8, query: dict = None):
        """ Creates a collection.
        """
        if query is None:
            query = {}
        query['name'] = __tmp8
        return __tmp0.session.post('/v4/collections/', data=query)

    def __tmp5(__tmp0, __tmp7):
        """ Deletes a collection.
        """
        return __tmp0.session.delete(
            f'/v4/collections/{__tmp7}/'
        )

    def collection_media_ids(__tmp0, __tmp7):
        """ Gets a list of the media assets ids of a collection.
        """
        return __tmp0.session.get(
            f'/v4/collections/{__tmp7}/media/'
        )

    def add_media_to_collection(__tmp0, __tmp7, __tmp3):
        """ Adds media assets to a collection.
        """
        query = {
            'data': json.dumps(__tmp3)
        }
        return __tmp0.session.post(
            f'/v4/collections/{__tmp7}/media/',
            data=query
        )

    def __tmp1(__tmp0, __tmp7, __tmp3: <FILL>):
        """ Removes media assets from a collection.
        """
        query = {
            'deleteIds': ','.join(map(str, __tmp3))
        }
        return __tmp0.session.delete(
            f'/v4/collections/{__tmp7}/media/',
            params=query
        )

    def __tmp2(__tmp0, __tmp7, collection_option,
                         __tmp6, query: dict = None):
        """ Shares a collection.
        """
        collection_options = ['view', 'edit']
        if collection_option not in collection_options:
            raise ValueError(
                f'Invalid collection_option. Expected one of: '
                f'{collection_options}'
            )
        if query is None:
            query = {}
        query['collectionOptions'] = collection_option
        query['recipients'] = ','.join(map(str, __tmp6))
        return __tmp0.session.post(
            f'/v4/collections/{__tmp7}/share/',
            data=query
        )
