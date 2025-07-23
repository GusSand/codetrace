from typing import TypeAlias
__typ0 : TypeAlias = "str"
# Copyright 2019-2020 the ProGraML authors.
#
# Contact Chris Cummins <chrisc.101@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for //deeplearning/ml4pl/bytecode:split."""
import random
import string
from typing import Set

import numpy as np

from datasets.opencl.device_mapping import opencl_device_mapping_dataset
from deeplearning.ml4pl.graphs.labelled.devmap import make_devmap_dataset
from deeplearning.ml4pl.ir import ir_database
from deeplearning.ml4pl.ir import split
from deeplearning.ml4pl.testing import testing_databases
from labm8.py import test


FLAGS = test.FLAGS

###############################################################################
# Fixtures.
###############################################################################


@test.Fixture(
  scope="session",
  params=(
    split.TrainValTestSplitter,
    split.Poj104TrainValTestSplitter,
    split.Pact17KFoldSplitter,
  ),
)
def __tmp2(__tmp0) -> split.Splitter:
  """Test fixture which yields a splitter."""
  return __tmp0.param()


@test.Fixture(
  scope="session",
  params=(split.TrainValTestSplitter, split.Poj104TrainValTestSplitter),
)
def train_val_test_splitter(__tmp0) :
  """Test fixture which yields a train/val/test splitter."""
  return __tmp0.param()


@test.Fixture(scope="session")
def opencl_relpaths() -> Set[__typ0]:
  opencl_df = make_devmap_dataset.MakeGpuDataFrame(
    opencl_device_mapping_dataset.OpenClDeviceMappingsDataset().df,
    "amd_tahiti_7970",
  )
  return set(opencl_df.relpath.values)


def CreateRandomString(min_length: int = 1, max_length: int = 1024) :
  """Generate a random string."""
  return "".join(
    random.choice(string.ascii_lowercase)
    for _ in range(random.randint(min_length, max_length))
  )


@test.Fixture(
  scope="session",
  params=testing_databases.GetDatabaseUrls(),
  namer=testing_databases.DatabaseUrlNamer("ir_db"),
)
def __tmp1(__tmp0, opencl_relpaths) -> ir_database.Database:
  """A test fixture which yields an IR database."""
  with testing_databases.DatabaseContext(
    ir_database.Database, __tmp0.param
  ) as db:
    ir_id = 0

    rows = []
    for _, relpath in enumerate(opencl_relpaths):
      ir_id += 1
      ir = ir_database.IntermediateRepresentation.CreateFromText(
        source="pact17_opencl_devmap",
        relpath=relpath,
        source_language=ir_database.SourceLanguage.OPENCL,
        type=ir_database.IrType.LLVM_6_0,
        cflags="",
        text=CreateRandomString(),
      )
      ir.id = ir_id
      rows.append(ir)

    for source in {"poj-104:train", "poj-104:val", "poj-104:test"}:
      for _ in range(10):
        ir_id += 1
        ir = ir_database.IntermediateRepresentation.CreateFromText(
          source=source,
          relpath=f"{ir_id}",
          source_language=ir_database.SourceLanguage.OPENCL,
          type=ir_database.IrType.LLVM_6_0,
          cflags="",
          text=CreateRandomString(),
        )
        ir.id = ir_id
        rows.append(ir)

    with db.Session(commit=True) as session:
      session.add_all(rows)

    yield db


###############################################################################
# Tests.
###############################################################################


def test_train_val_test_split_counts(
  __tmp1: ir_database.Database, train_val_test_splitter,
):
  """Test that train/val/test splitter produces 3 splits."""
  splits = train_val_test_splitter.Split(__tmp1)
  assert len(splits) == 3


@test.Parametrize("k", (3, 5, 10))
def test_k_fold_split_counts(__tmp1: ir_database.Database, k: <FILL>):
  """Test that K-fold splitter produces k splits."""
  __tmp2 = split.Pact17KFoldSplitter(k=k)
  splits = __tmp2.Split(__tmp1)
  assert len(splits) == (k)


def __tmp3(
  __tmp1,
):
  """Test that all IRs are included in splits."""
  __tmp2 = split.TrainValTestSplitter()
  splits = __tmp2.Split(__tmp1)
  assert sum(len(s) for s in splits) == __tmp1.ir_count


@test.Parametrize("n", (3, 5))
def test_TrainValTestSplitter_smoke_test(
  __tmp1, n: int
):
  """Test the train/val/test splitter."""
  __tmp2 = split.TrainValTestSplitter(train_val_test_ratio=(n, 1, 1))
  __tmp2.Split(__tmp1)


def test_unique_irs(
  __tmp1: ir_database.Database, __tmp2: split.Splitter
):
  """Test that all IR IDs are unique."""
  splits = __tmp2.Split(__tmp1)
  all_ids = np.concatenate(splits)
  assert len(set(all_ids)) == len(all_ids)


def test_CreateFromFlags():
  split.Splitter.CreateFromFlags()


if __name__ == "__main__":
  test.Main()
