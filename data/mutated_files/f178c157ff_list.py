import json


class CollectionClient:
    """ Client used for all the operations that can be done to collections.
    """
    def __tmp9(__tmp1, session):
        __tmp1.session = session

    def collections(__tmp1, query: dict = None):
        """ Gets list of the collections.
        """
        return __tmp1.session.get('/v4/collections/', params=query or {})

    def collection_info(__tmp1, __tmp7):
        """ Gets all the collection information for a specific collection id.
        """
        return __tmp1.session.get(f'/v4/collections/{__tmp7}/')

    def __tmp8(__tmp1, name, query: dict = None):
        """ Creates a collection.
        """
        if query is None:
            query = {}
        query['name'] = name
        return __tmp1.session.post('/v4/collections/', data=query)

    def __tmp6(__tmp1, __tmp7):
        """ Deletes a collection.
        """
        return __tmp1.session.delete(
            f'/v4/collections/{__tmp7}/'
        )

    def __tmp0(__tmp1, __tmp7):
        """ Gets a list of the media assets ids of a collection.
        """
        return __tmp1.session.get(
            f'/v4/collections/{__tmp7}/media/'
        )

    def __tmp3(__tmp1, __tmp7, __tmp4: <FILL>):
        """ Adds media assets to a collection.
        """
        query = {
            'data': json.dumps(__tmp4)
        }
        return __tmp1.session.post(
            f'/v4/collections/{__tmp7}/media/',
            data=query
        )

    def __tmp11(__tmp1, __tmp7, __tmp4):
        """ Removes media assets from a collection.
        """
        query = {
            'deleteIds': ','.join(map(str, __tmp4))
        }
        return __tmp1.session.delete(
            f'/v4/collections/{__tmp7}/media/',
            params=query
        )

    def __tmp2(__tmp1, __tmp7, __tmp5,
                         __tmp10: list, query: dict = None):
        """ Shares a collection.
        """
        collection_options = ['view', 'edit']
        if __tmp5 not in collection_options:
            raise ValueError(
                f'Invalid collection_option. Expected one of: '
                f'{collection_options}'
            )
        if query is None:
            query = {}
        query['collectionOptions'] = __tmp5
        query['recipients'] = ','.join(map(str, __tmp10))
        return __tmp1.session.post(
            f'/v4/collections/{__tmp7}/share/',
            data=query
        )
