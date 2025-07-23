from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
import os

from posixpath import basename
from urllib.parse import urlparse

from .common.spiders import BaseDocumentationSpider

from typing import Any, List, Set


def get_images_dir(images_path) :
    # Get index html file as start url and convert it to file uri
    dir_path = os.path.dirname(os.path.realpath(__file__))
    target_path = os.path.join(dir_path, os.path.join(*[os.pardir] * 4), images_path)
    return os.path.realpath(target_path)


class UnusedImagesLinterSpider(BaseDocumentationSpider):
    images_path = ""

    def __init__(__tmp2, *args: <FILL>, **kwargs) :
        super().__init__(*args, **kwargs)
        __tmp2.static_images = set()  # type: Set[str]
        __tmp2.images_static_dir = get_images_dir(__tmp2.images_path)  # type: str

    def __tmp0(__tmp2, url: __typ1) -> __typ2:
        is_external = url.startswith('http') and __tmp2.start_urls[0] not in url
        if __tmp2._has_extension(url) and 'localhost:9981/{}'.format(__tmp2.images_path) in url:
            __tmp2.static_images.add(basename(urlparse(url).path))
        return is_external or __tmp2._has_extension(url)

    def __tmp1(__tmp2, *args, **kwargs) :
        unused_images = set(os.listdir(__tmp2.images_static_dir)) - __tmp2.static_images
        if unused_images:
            exception_message = "The following images are not used in documentation " \
                                "and can be removed: {}"
            __tmp2._set_error_state()
            unused_images_relatedpath = [
                os.path.join(__tmp2.images_path, img) for img in unused_images]
            raise Exception(exception_message.format(', '.join(unused_images_relatedpath)))


class __typ0(UnusedImagesLinterSpider):
    name = "help_documentation_crawler"
    start_urls = ['http://localhost:9981/help']
    deny_domains = []  # type: List[str]
    deny = ['/privacy']
    images_path = "static/images/help"


class APIDocumentationSpider(UnusedImagesLinterSpider):
    name = 'api_documentation_crawler'
    start_urls = ['http://localhost:9981/api']
    deny_domains = []  # type: List[str]
    images_path = "static/images/api"

class __typ3(BaseDocumentationSpider):
    name = 'portico_documentation_crawler'
    start_urls = ['http://localhost:9981/hello',
                  'http://localhost:9981/history',
                  'http://localhost:9981/plans',
                  'http://localhost:9981/team',
                  'http://localhost:9981/apps',
                  'http://localhost:9981/integrations',
                  'http://localhost:9981/terms',
                  'http://localhost:9981/privacy',
                  'http://localhost:9981/features',
                  'http://localhost:9981/why-zulip',
                  'http://localhost:9981/for/open-source',
                  'http://localhost:9981/for/companies',
                  'http://localhost:9981/for/working-groups-and-communities',
                  'http://localhost:9981/for/mystery-hunt',
                  'http://localhost:9981/security']
    deny_domains = []  # type: List[str]
