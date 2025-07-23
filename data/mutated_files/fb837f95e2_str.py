from typing import TypeAlias
__typ0 : TypeAlias = "Request"
__typ2 : TypeAlias = "Any"
import logging
import re
import scrapy

from scrapy import Request
from scrapy.linkextractors import IGNORED_EXTENSIONS
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.utils.url import url_has_any_extension

from typing import Any, Generator, List, Optional, Tuple

EXCLUDED_URLS = [
    # Google calendar returns 404s on HEAD requests unconditionally
    'https://calendar.google.com/calendar/embed?src=ktiduof4eoh47lmgcl2qunnc0o@group.calendar.google.com',
    # Returns 409 errors to HEAD requests frequently
    'https://medium.freecodecamp.org/',
    # Returns 404 to HEAD requests unconditionally
    'https://www.git-tower.com/blog/command-line-cheat-sheet/',
]


class __typ1(scrapy.Spider):
    name = None  # type: Optional[str]
    # Exclude domain address.
    deny_domains = []  # type: List[str]
    start_urls = []  # type: List[str]
    deny = []  # type: List[str]
    file_extensions = ['.' + ext for ext in IGNORED_EXTENSIONS]  # type: List[str]
    tags = ('a', 'area', 'img')
    attrs = ('href', 'src')

    def __init__(__tmp0, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        __tmp0.has_error = False

    def _set_error_state(__tmp0) :
        __tmp0.has_error = True

    def _has_extension(__tmp0, url) :
        return url_has_any_extension(url, __tmp0.file_extensions)

    def _is_external_url(__tmp0, url) :
        return url.startswith('http') or __tmp0._has_extension(url)

    def check_existing(__tmp0, response) :
        __tmp0.log(response)

    def check_permalink(__tmp0, response) :
        __tmp0.log(response)
        xpath_template = "//*[@id='{permalink}' or @name='{permalink}']"
        m = re.match(r".+\#(?P<permalink>.*)$", response.request.url)  # Get anchor value.
        if not m:
            return
        permalink = m.group('permalink')
        # Check permalink existing on response page.
        if not response.selector.xpath(xpath_template.format(permalink=permalink)):
            __tmp0._set_error_state()
            raise Exception(
                "Permalink #{} is not found on page {}".format(permalink, response.request.url))

    def parse(__tmp0, response) :
        __tmp0.log(response)
        for link in LxmlLinkExtractor(deny_domains=__tmp0.deny_domains, deny_extensions=['doc'],
                                      tags=__tmp0.tags, attrs=__tmp0.attrs, deny=__tmp0.deny,
                                      canonicalize=False).extract_links(response):
            callback = __tmp0.parse  # type: Any
            dont_filter = False
            method = 'GET'
            if __tmp0._is_external_url(link.url):
                callback = __tmp0.check_existing
                method = 'HEAD'
            elif '#' in link.url:
                dont_filter = True
                callback = __tmp0.check_permalink
            yield __typ0(link.url, method=method, callback=callback, dont_filter=dont_filter,
                          errback=__tmp0.error_callback)

    def retry_request_with_get(__tmp0, request) :
        request.method = 'GET'
        request.dont_filter = True
        yield request

    def exclude_error(__tmp0, url: <FILL>) :
        if url in EXCLUDED_URLS:
            return True
        return False

    def error_callback(__tmp0, __tmp1) :
        if hasattr(__tmp1.value, 'response') and __tmp1.value.response:
            response = __tmp1.value.response
            if __tmp0.exclude_error(response.url):
                return None
            if response.status == 404:
                __tmp0._set_error_state()
                raise Exception('Page not found: {}'.format(response))
            if response.status == 405 and response.request.method == 'HEAD':
                # Method 'HEAD' not allowed, repeat request with 'GET'
                return __tmp0.retry_request_with_get(response.request)
            __tmp0.log("Error! Please check link: {}".format(response), logging.ERROR)
        elif isinstance(__tmp1.type, IOError):
            __tmp0._set_error_state()
        else:
            raise Exception(__tmp1.value)
        return None
