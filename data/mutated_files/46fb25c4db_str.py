from typing import TypeAlias
__typ0 : TypeAlias = "dict"
from bynder_sdk.client.upload_client import UploadClient


class AssetBankClient:
    """ Client used for all the operations that can be done to the
    Bynder Asset Bank.
    """
    def __tmp14(__tmp3, session):
        __tmp3.session = session
        __tmp3.upload_client = UploadClient(session)

    def __tmp9(__tmp3):
        """ Gets list of the brands.
        """
        return __tmp3.session.get('/v4/brands/')

    def __tmp11(__tmp3, query: __typ0 = None):
        """ Gets list of the tags.
        """
        return __tmp3.session.get('/v4/tags/', params=query or {})

    def __tmp4(__tmp3, query: __typ0 = None):
        """ Gets list of the meta properties.
        """
        return __tmp3.session.get('/v4/metaproperties/', params=query or {})

    def __tmp13(__tmp3, query: __typ0 = None):
        """ Gets a list of media assets filtered by parameters.
        """
        return __tmp3.session.get('/v4/media/', params=query or {})

    def __tmp6(__tmp3, __tmp10, versions: __typ0 = None):
        """ Gets all the media information for a specific media id.
        """
        return __tmp3.session.get(
            f'/v4/media/{__tmp10}/',
            params=versions or {}
        )

    def __tmp2(__tmp3, __tmp10, query: __typ0 = None):
        """ Gets the download file URL for a specific media id.
        """
        return __tmp3.session.get(
            f'/v4/media/{__tmp10}/download/',
            params=query or {}
        )

    def __tmp1(__tmp3, __tmp10, query: __typ0 = None):
        """ Updates the media properties (metadata) for a specific media id.
        """
        return __tmp3.session.post(
            f'/v4/media/{__tmp10}/',
            data=query or {}
        )

    def __tmp0(__tmp3, __tmp10):
        """ Deletes a media asset.
        """
        return __tmp3.session.delete(f'/v4/media/{__tmp10}/')

    def __tmp17(__tmp3, __tmp7, __tmp16, query: __typ0 = None):
        """ Creates a usage record for a media asset.
        """
        if query is None:
            query = {}
        query['integration_id'] = __tmp7
        query['asset_id'] = __tmp16

        return __tmp3.session.post('/media/usage/', data=query)

    def __tmp8(__tmp3, query: __typ0 = None):
        """ Gets all the media assets usage records.
        """
        return __tmp3.session.get('/media/usage/', params=query or {})

    def delete_usage(__tmp3, __tmp7, __tmp16, query: __typ0 = None):
        """ Deletes a usage record of a media asset.
        """
        if query is None:
            query = {}
        query['integration_id'] = __tmp7
        query['asset_id'] = __tmp16

        return __tmp3.session.delete('/media/usage/', params=query)

    def __tmp5(__tmp3, __tmp12, __tmp15: <FILL>,
                    __tmp10: str = '', query: __typ0 = None) :
        """ Upload file.
            Params:
                file_path: the local filepath of the file to upload.
                brand_id: the brandid of the brand that belong the asset.
                query: extra dict parameters of information to add to the
                       asset. (See api documentation for more information)
            Return a dict with the keys:
                - success: boolean that indicate the result of the upload call.
                - mediaitems: a list of mediaitems created, with at least the
                    original.
                - batchId: the batchId of the upload.
                - mediaid: the mediaId update or created.
        """
        if query is None:
            query = {}
        query['brandId'] = __tmp15
        return __tmp3.upload_client.upload(
            __tmp12=__tmp12,
            __tmp10=__tmp10,
            upload_data=query
        )
