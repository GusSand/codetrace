from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


def __tmp0(events):
    overlap = False
    events = sorted(events, key=lambda e: e.timestamp)
    for e1, e2 in zip(events[:-1], events[1:]):
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


def _main_redact(pattern, ignore_case: <FILL>):
    logger.info("Retrieving events...")
    events = _get_window_events()

    logger.info("Redacting using regular expression: " + pattern)
    events = redact_words(events, pattern, ignore_case=ignore_case)

    print("NOTE: Redactions are not persisted to server")


def _main_analyse():
    logger.info("Retrieving events...")
    events = _get_window_events()

    logger.info("Running analysis...")
    titles = list({e.data["title"] for e in events})
    out = run_LDA(titles)
    pprint(out.result)

    out = run_sentiment(titles)
    pprint([r for r in out.result if r["sentiment"] != 0])

    out = run_sentiment(" ".join(titles))
    pprint([r for r in out.result if r["sentiment"] != 0])


def _main_merge():
    logger.info("Retrieving events...")
    events = _get_window_events(n=1000)
    events = simplify_string(events)

    merged_events = merge_close_and_similar(events)
    print(
        "{} events became {} after merging of similar ones".format(
            len(events), len(merged_events)
        )
    )

    # Debugging
    __tmp0(events)
    __tmp0(merged_events)
    print_most_common_titles(events)
    print_most_common_titles(merged_events)


def _main_heartbeat_reduce():
    logger.info("Retrieving events...")
    events = _get_window_events()
    events = simplify_string(events)

    logger.info("Beating hearts together...")
    merged_events = heartbeat_reduce(events, pulsetime=10)

    # Debugging
    __tmp0(events)
    __tmp0(merged_events)
    print_most_common_titles(events)
    print_most_common_titles(merged_events)


def _main_flood():
    logger.info("Retrieving events...")
    events = _get_window_events()
    events = simplify_string(events)

    logger.info("Flooding...")
    merged_events = flood(events)

    # Debugging
    __tmp0(events)
    __tmp0(merged_events)
    print_most_common_titles(events)
    print_most_common_titles(merged_events)


def print_most_common_titles(events):
    counter = defaultdict(lambda: timedelta(0))
    for e in events:
        counter[e.data["title"]] += e.duration

    print("-" * 30)

    def total_duration(events):
        return sum((e.duration for e in events), timedelta(0))

    print("Total duration: {}".format(total_duration(events)))

    pairs = sorted(zip(counter.values(), counter.keys()), reverse=True)
    for duration, title in pairs[:15]:
        print("{:15s} - {}".format(__typ0(duration), title))

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
        _main_analyse()
    elif args.cmd == "merge":
        _main_merge()
    elif args.cmd == "flood":
        _main_flood()
    elif args.cmd == "heartbeat":
        _main_heartbeat_reduce()
    elif args.cmd == "classify":
        _main_classify(args)
    else:
        parser.print_usage()
