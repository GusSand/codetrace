from typing import TypeAlias
__typ3 : TypeAlias = "bool"
# Copyright (c) 2016-2020 Chris Cummins.
#
# clgen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# clgen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with clgen.  If not, see <https://www.gnu.org/licenses/>.
"""This file contains the SampleObserver interface and concrete subclasses."""
import pathlib

from deeplearning.clgen.proto import model_pb2
from labm8.py import app
from labm8.py import crypto
from labm8.py import fs
from labm8.py import pbutil

FLAGS = app.FLAGS


class __typ6(object):
  """An observer that is notified when new samples are produced.

  During sampling of a model, sample observers are notified for each new
  sample produced. Additionally, sample observers determine when to terminate
  sampling.
  """

  def Specialize(__tmp2, model, __tmp3) :
    """Specialize the sample observer to a model and sampler combination.

    This enables the observer to set state specialized to a specific model and
    sampler. This is guaranteed to be called before OnSample(), and
    sets that the model and sampler for each subsequent call to OnSample(),
    until the next call to Specialize().

    Subclasses do not need to override this method.

    Args:
      model: The model that is being sampled.
      sampler: The sampler that is being used.
    """
    pass

  def __tmp0(__tmp2, sample) :
    """Sample notification callback.

    Args:
      sample: The newly created sample message.

    Returns:
      True if sampling should continue, else False. Batching of samples means
      that returning False does not guarantee that sampling will terminate
      immediately, and OnSample() may be called again.
    """
    raise NotImplementedError("abstract class")


class __typ4(__typ6):
  """An observer that terminates sampling after a finite number of samples."""

  def __tmp1(__tmp2, min_sample_count: <FILL>):
    if min_sample_count <= 0:
      raise ValueError(
        f"min_sample_count must be >= 1. Received: {min_sample_count}"
      )

    __tmp2._sample_count = 0
    __tmp2._min_sample_count = min_sample_count

  def __tmp0(__tmp2, sample: model_pb2.Sample) :
    """Sample receive callback. Returns True if sampling should continue."""
    __tmp2._sample_count += 1
    return __tmp2._sample_count < __tmp2._min_sample_count


class __typ5(__typ6):
  """An observer that creates a file of the sample text for each sample."""

  def __tmp1(__tmp2, path):
    __tmp2.path = pathlib.Path(path)
    __tmp2.path.mkdir(parents=True, exist_ok=True)

  def __tmp0(__tmp2, sample) :
    """Sample receive callback. Returns True if sampling should continue."""
    sample_id = crypto.sha256_str(sample.text)
    path = __tmp2.path / f"{sample_id}.txt"
    fs.Write(path, sample.text.encode("utf-8"))
    return True


class __typ0(__typ6):
  """An observer that prints the text of each sample that is generated."""

  def __tmp0(__tmp2, sample) :
    """Sample receive callback. Returns True if sampling should continue."""
    print(f"=== CLGEN SAMPLE ===\n\n{sample.text}\n")
    return True


class __typ2(__typ6):
  """An observer that saves all samples in-memory."""

  def __tmp1(__tmp2):
    __tmp2.samples = []

  def __tmp0(__tmp2, sample: model_pb2.Sample) :
    """Sample receive callback. Returns True if sampling should continue."""
    __tmp2.samples.append(sample)
    return True


class __typ1(__typ6):
  """Backwards compatability implementation of the old sample caching behavior.

  In previous versions of CLgen, model sampling would silently (and always)
  create sample protobufs in the sampler cache, located at:

    CLGEN_CACHE/models/MODEL/samples/SAMPLER

  This sample observer provides equivalent behavior.
  """

  def __tmp1(__tmp2):
    __tmp2.cache_path = None

  def Specialize(__tmp2, model, __tmp3) -> None:
    """Specialize observer to a model and sampler combination."""
    __tmp2.cache_path = model.SamplerCache(__tmp3)
    __tmp2.cache_path.mkdir(exist_ok=True)

  def __tmp0(__tmp2, sample) :
    """Sample receive callback. Returns True if sampling should continue."""
    sample_id = crypto.sha256_str(sample.text)
    sample_path = __tmp2.cache_path / f"{sample_id}.pbtxt"
    pbutil.ToFile(sample, sample_path)
    return True
