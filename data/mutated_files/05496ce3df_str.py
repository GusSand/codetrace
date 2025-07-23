import logging
import argparse
from typing import List, Pattern
from pprint import pprint
from collections import defaultdict
from datetime import timedelta

from aw_transform import heartbeat_reduce
from aw_transform.flood import flood
from aw_transform.simplify import simplify_string

from aw_client import ActivityWatchClient

from aw_research.redact import redact_words
from aw_research.algorithmia import run_sentiment, run_LDA
from aw_research.merge import merge_close_and_similar
from aw_research.classify import _main as _main_classify
from aw_research.classify import _build_argparse as _build_argparse_classify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def assert_no_overlap(__tmp1):
    overlap = False
    __tmp1 = sorted(__tmp1, key=lambda e: e.timestamp)
    for e1, e2 in zip(__tmp1[:-1], __tmp1[1:]):
        e1_end = e1.timestamp + e1.duration
        gap = e2.timestamp - e1_end
        if gap < timedelta(0):
            logger.warning("Events overlapped: {}".format(gap))
            overlap = True
    assert not overlap


def _get_window_events(n=1000):
    client = ActivityWatchClient("aw-analyser", testing=True)
    buckets = client.get_buckets()

    bucket_id = None
    for _bid in buckets.keys():
        if "window" in _bid and "testing" not in _bid:
            bucket_id = _bid

    if bucket_id:
        return client.get_events(bucket_id, limit=n)
    else:
        print("Did not find bucket")
        return []


def _main_redact(pattern: <FILL>, ignore_case):
    logger.info("Retrieving events...")
    __tmp1 = _get_window_events()

    logger.info("Redacting using regular expression: " + pattern)
    __tmp1 = redact_words(__tmp1, pattern, ignore_case=ignore_case)

    print("NOTE: Redactions are not persisted to server")


def __tmp2():
    logger.info("Retrieving events...")
    __tmp1 = _get_window_events()

    logger.info("Running analysis...")
    titles = list({e.data["title"] for e in __tmp1})
    out = run_LDA(titles)
    pprint(out.result)

    out = run_sentiment(titles)
    pprint([r for r in out.result if r["sentiment"] != 0])

    out = run_sentiment(" ".join(titles))
    pprint([r for r in out.result if r["sentiment"] != 0])


def _main_merge():
    logger.info("Retrieving events...")
    __tmp1 = _get_window_events(n=1000)
    __tmp1 = simplify_string(__tmp1)

    merged_events = merge_close_and_similar(__tmp1)
    print(
        "{} events became {} after merging of similar ones".format(
            len(__tmp1), len(merged_events)
        )
    )

    # Debugging
    assert_no_overlap(__tmp1)
    assert_no_overlap(merged_events)
    print_most_common_titles(__tmp1)
    print_most_common_titles(merged_events)


def __tmp0():
    logger.info("Retrieving events...")
    __tmp1 = _get_window_events()
    __tmp1 = simplify_string(__tmp1)

    logger.info("Beating hearts together...")
    merged_events = heartbeat_reduce(__tmp1, pulsetime=10)

    # Debugging
    assert_no_overlap(__tmp1)
    assert_no_overlap(merged_events)
    print_most_common_titles(__tmp1)
    print_most_common_titles(merged_events)


def _main_flood():
    logger.info("Retrieving events...")
    __tmp1 = _get_window_events()
    __tmp1 = simplify_string(__tmp1)

    logger.info("Flooding...")
    merged_events = flood(__tmp1)

    # Debugging
    assert_no_overlap(__tmp1)
    assert_no_overlap(merged_events)
    print_most_common_titles(__tmp1)
    print_most_common_titles(merged_events)


def print_most_common_titles(__tmp1):
    counter = defaultdict(lambda: timedelta(0))
    for e in __tmp1:
        counter[e.data["title"]] += e.duration

    print("-" * 30)

    def total_duration(__tmp1):
        return sum((e.duration for e in __tmp1), timedelta(0))

    print("Total duration: {}".format(total_duration(__tmp1)))

    pairs = sorted(zip(counter.values(), counter.keys()), reverse=True)
    for duration, title in pairs[:15]:
        print("{:15s} - {}".format(str(duration), title))

    print("-" * 30)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")
    redact = subparsers.add_parser("redact")
    redact.add_argument(
        "pattern",
        help="Regular expression to match events with, a good example that matches on 3 words: \b(sensitive|secret|)\b",
    )
    redact.add_argument(
        "--ignore-case",
        action="store_true",
        help="Ignore case sensitivity (the pattern and all strings are lowercased before matching)",
    )
    subparsers.add_parser("analyse")
    subparsers.add_parser("merge")
    subparsers.add_parser("flood")
    subparsers.add_parser("heartbeat")
    classify = subparsers.add_parser("classify")
    _build_argparse_classify(classify)

    args = parser.parse_args()

    if args.cmd == "redact":
        _main_redact(args.pattern, args.ignore_case)
    elif args.cmd == "analyse":
        __tmp2()
    elif args.cmd == "merge":
        _main_merge()
    elif args.cmd == "flood":
        _main_flood()
    elif args.cmd == "heartbeat":
        __tmp0()
    elif args.cmd == "classify":
        _main_classify(args)
    else:
        parser.print_usage()
