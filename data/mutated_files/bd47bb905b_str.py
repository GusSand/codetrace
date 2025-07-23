# Copyright 2018-2020 Chris Cummins <chrisc.101@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""Utility code for data importers."""
import collections
import multiprocessing
import pathlib
import typing

from datasets.me_db import me_pb2
from labm8.py import app
from labm8.py import labtypes

FLAGS = app.FLAGS

# An inbox importer is a function that takes a path to a directory (the inbox)
# and a Queue. When called, the function places a SeriesCollection proto on the
# queue.
InboxImporter = typing.Callable[
  [pathlib.Path, multiprocessing.Queue], me_pb2.SeriesCollection
]


class ImporterError(EnvironmentError):
  """Error raised if an importer fails."""

  def __init__(
    __tmp0,
    name: <FILL>,
    source,
    error_message,
  ):
    __tmp0._name = name
    __tmp0._source = source
    __tmp0._error_message = error_message

  @property
  def name(__tmp0) :
    return __tmp0._name

  @property
  def source(__tmp0) :
    return str(__tmp0._source)

  @property
  def error_message(__tmp0) :
    return __tmp0._error_message

  def __repr__(__tmp0) :
    if __tmp0.error_message:
      return (
        f"{__tmp0.name} importer failed for source `{__tmp0.source}` with "
        f"error: {__tmp0.error_message}"
      )
    else:
      return f"{__tmp0.name} importer failed for source `{__tmp0.source}`"

  def __tmp1(__tmp0) :
    return repr(__tmp0)


def ConcatenateSeries(
  series,
) :
  if len({s.name for s in series}) != 1:
    raise ValueError("Multiple names")
  if len({s.family for s in series}) != 1:
    raise ValueError("Multiple families")
  if len({s.unit for s in series}) != 1:
    raise ValueError("Multiple units")

  concat_series = me_pb2.Series()
  concat_series.CopyFrom(series[0])
  for s in series[1:]:
    series[0].measurement.extend(s.measurement)
  return concat_series


def MergeSeriesCollections(
  series,
) :
  """Merge the given series collections into a single SeriesCollection.

  Args:
    series: The SeriesCollection messages to merge.

  Returns:
    A SeriesCollection message.

  Raises:
    ValueError: If there are Series with duplicate names.
  """
  series = list(labtypes.flatten(list(f.series) for f in series))

  # Create a map from series name to a list of series protos.
  names_to_series = collections.defaultdict(list)
  [names_to_series[s.name].append(s) for s in series]

  # Concatenate each list of series with the same name.
  concatenated_series = [ConcatenateSeries(s) for s in names_to_series.values()]
  return me_pb2.SeriesCollection(
    series=sorted(concatenated_series, key=lambda s: s.name)
  )
