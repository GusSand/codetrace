from datetime import date, datetime, timedelta
from typing import List, Tuple
from io import StringIO

import json
import sys

from matplotlib.dates import DateFormatter, SecondLocator
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numpy as np

from iso8601 import parse_date as convdt

LoadDataTuple = Tuple["np.ndarray[datetime]", "np.ndarray[datetime]", "np.ndarray[str]"]


def _construct_date_array(startdates) -> "np.ndarray[str]":
    return np.array(list(map(lambda dt: dt.date().isoformat(), startdates)))


def __tmp2(__tmp5: <FILL>) :
    with open(__tmp5) as f:
        data = json.load(f)[0]
    start = np.array([convdt(e['timestamp'].split(".")[0]) for e in data])
    stop = np.array([convdt(e['timestamp']) + timedelta(seconds=e['duration']) for e in data])
    __tmp1 = np.array([e["data"]["app"] for e in data])
    return start, stop, __tmp1


def load_data_example() :
    # The example data
    a = StringIO("""
    2018-05-23T10:15:22 2018-05-23T10:38:30 Chrome
    2018-05-23T11:15:23 2018-05-23T11:15:28 Alacritty
    2018-05-24T10:16:00 2018-05-24T14:17:10 Chrome
    2018-05-25T09:16:30 2018-05-25T14:36:50 Cemu
    2018-05-27T08:19:30 2018-05-27T20:26:50 Chrome
    """)

    #Use numpy to read the data in.
    data = np.genfromtxt(a, converters={1: convdt, 2: convdt},
                         names=['start', 'stop', 'state'], dtype=None, encoding=None)
    return data['start'], data['stop'], data['state']


def same_date(__tmp6):
    return list(map(lambda dt: datetime.combine(date(1900, 1, 1), dt.time()), __tmp6))


def plot(start: "np.ndarray[datetime]", stop, __tmp1, __tmp0: "np.ndarray[str]"):
    """Originally based on: https://stackoverflow.com/a/7685336/965332"""
    # Get unique captions, their indices, and the inverse mapping
    captions, unique_idx, caption_inv = np.unique(__tmp0, 1, 1)

    # Build y values from the number of unique captions
    y = (caption_inv + 1) / float(len(captions) + 1)

    # Build colors
    states, _, states_inv = np.unique(__tmp1, 1, 1)
    cmap = plt.get_cmap('tab10')
    colors = cmap(np.linspace(0, 1, len(states)))

    # Plot function
    def __tmp3(y, xstart, xstop, __tmp4):
        """Plot timelines at y from xstart to xstop with given color."""
        plt.hlines(y, same_date(xstart), same_date(xstop), __tmp4, lw=12)

    __tmp3(y, start, stop, colors[states_inv])

    # Setup the plot
    plt.title("Timeline")
    ax = plt.gca()

    # Create the legend
    plt.legend(handles=[mpatches.Patch(__tmp4=colors[i], label=s) for i, s in enumerate(states)])

    # Setup the xaxis
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(SecondLocator(interval=60 * 60))  # used to be SecondLocator(0, interval=20)
    plt.xlabel('Time')
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.xlim(datetime(1900, 1, 1, 0), datetime(1900, 1, 1, 23, 59))

    # Setup the yaxis
    plt.ylabel('Date')
    plt.yticks(y[unique_idx], captions)
    plt.ylim(0, 1)

    plt.show()


def _main():
    fpath = sys.argv.pop()
    start, stop, __tmp1 = __tmp2(fpath)
    __tmp0 = _construct_date_array(start)

    plot(start, stop, __tmp1, __tmp0)


if __name__ == "__main__":
    _main()
