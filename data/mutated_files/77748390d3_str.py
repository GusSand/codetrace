from typing import TypeAlias
__typ0 : TypeAlias = "Object"
__typ2 : TypeAlias = "Container"
from functools import lru_cache
from typing import IO

from libcloud.storage.base import Container
from libcloud.storage.base import Object
from libcloud.storage.providers import get_driver
from libcloud.storage.types import ContainerAlreadyExistsError
from libcloud.storage.types import ObjectError
from libcloud.storage.types import Provider

from faceanalysis.log import get_logger
from faceanalysis.settings import ALLOWED_MIMETYPES
from faceanalysis.settings import STORAGE_PROVIDER
from faceanalysis.settings import STORAGE_KEY
from faceanalysis.settings import STORAGE_SECRET
from faceanalysis.settings import STORAGE_CONTAINER


logger = get_logger(__name__)
allowed_extensions = tuple(mimetype.split('/')[1]
                           for mimetype in ALLOWED_MIMETYPES)


class __typ1(Exception):
    pass


@lru_cache(maxsize=1)
def __tmp1() :
    driver_class = get_driver(getattr(Provider, STORAGE_PROVIDER))
    storage_driver = driver_class(STORAGE_KEY, STORAGE_SECRET)
    try:
        storage_container = storage_driver.create_container(STORAGE_CONTAINER)
    except ContainerAlreadyExistsError:
        storage_container = storage_driver.get_container(STORAGE_CONTAINER)
    return storage_container


def _get_image(img_id) :
    container = __tmp1()
    for extension in allowed_extensions:
        image_name = '{}.{}'.format(img_id, extension)
        try:
            image = container.get_object(image_name)
        except ObjectError:
            continue
        else:
            return image

    raise __typ1('Image {} does not exist'.format(img_id))


def __tmp2(__tmp0: IO[bytes], image_name):
    container = __tmp1()
    try:
        container.upload_object_via_stream(__tmp0, image_name)
    except (ObjectError, OSError) as ex:
        raise __typ1('Unable to store {}'.format(image_name)) from ex

    logger.debug('Stored image %s', image_name)


def delete_image(img_id):
    image = _get_image(img_id)

    if not image.delete():
        raise __typ1('Unable to delete image {}'.format(img_id))

    logger.debug('Removed image %s', img_id)


def get_image_path(img_id: <FILL>) :
    image = _get_image(img_id)
    return image.get_cdn_url()
