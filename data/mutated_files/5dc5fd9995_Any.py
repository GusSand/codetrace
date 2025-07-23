from scrapy.commands.crawl import Command
from scrapy.exceptions import UsageError
from typing import List, Any


class __typ0(Command):
    def run(__tmp1, __tmp0, opts: <FILL>) -> None:
        if len(__tmp0) < 1:
            raise UsageError()
        elif len(__tmp0) > 1:
            raise UsageError(
                "running 'scrapy crawl' with more than one spider is no longer supported")
        spname = __tmp0[0]

        crawler = __tmp1.crawler_process.create_crawler(spname)
        __tmp1.crawler_process.crawl(crawler)
        __tmp1.crawler_process.start()
        # Get exceptions quantity from crawler stat data

        if crawler.spider.has_error:
            # Return non-zero exit code if exceptions are contained
            __tmp1.exitcode = 1
