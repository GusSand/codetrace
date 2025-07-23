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
"""Utilities for working with LLVM statements."""
import difflib
import re
import typing

import networkx as nx

from deeplearning.ml4pl.graphs import nx_utils
from deeplearning.ml4pl.graphs import programl_pb2
from deeplearning.ncc import rgx_utils as rgx
from deeplearning.ncc.inst2vec import inst2vec_preprocess
from labm8.py import app


FLAGS = app.FLAGS


def __tmp3(g, __tmp8: <FILL>) :
  for node, data in g.nodes(data=True):
    if data["type"] != programl_pb2.Node.STATEMENT:
      continue
    if " = alloca " in data["text"]:
      allocated_identifier = data["text"].split(" =")[0]
      if allocated_identifier == __tmp8:
        return node
  raise ValueError(
    f"Unable to find `alloca` statement for identifier `{__tmp8}`"
  )


def __tmp4(__tmp1: str) -> str:
  """This is a copy of inst2vec_preprocess.PreprocessStatement(), but instead
  of substituting placeholders values, immediates and labels are removed
  entirely from the string.
  """
  # Remove local identifiers
  __tmp1 = re.sub(rgx.local_id, "", __tmp1)
  # Global identifiers
  __tmp1 = re.sub(rgx.global_id, "", __tmp1)
  # Remove labels
  if re.match(r"; <label>:\d+:?(\s+; preds = )?", __tmp1):
    __tmp1 = re.sub(r":\d+", ":", __tmp1)
  elif re.match(rgx.local_id_no_perc + r":(\s+; preds = )?", __tmp1):
    __tmp1 = re.sub(rgx.local_id_no_perc + ":", ":", __tmp1)

  # Remove floating point values
  __tmp1 = re.sub(rgx.immediate_value_float_hexa, "", __tmp1)
  __tmp1 = re.sub(rgx.immediate_value_float_sci, "", __tmp1)

  # Remove integer values
  if (
    re.match("<%ID> = extractelement", __tmp1) is None
    and re.match("<%ID> = extractvalue", __tmp1) is None
    and re.match("<%ID> = insertelement", __tmp1) is None
    and re.match("<%ID> = insertvalue", __tmp1) is None
  ):
    __tmp1 = re.sub(r"(?<!align)(?<!\[) " + rgx.immediate_value_int, " ", __tmp1)

  # Remove string values
  __tmp1 = re.sub(rgx.immediate_value_string, " ", __tmp1)

  # Remove index types
  if (
    re.match(" = extractelement", __tmp1) is not None
    or re.match(" = insertelement", __tmp1) is not None
  ):
    __tmp1 = re.sub(r"i\d+ ", " ", __tmp1)

  return __tmp1


def __tmp0(
  __tmp7: str,
) -> typing.Tuple[str, typing.List[str]]:
  """Get the destination identifier for an LLVM statement (if any), and a list
  of operand identifiers (if any).
  """
  # Left hand side.
  destination = ""
  if "=" in __tmp7:
    first_equals = __tmp7.index("=")
    destination = __tmp7[:first_equals]
    __tmp7 = __tmp7[first_equals:]

  # Strip the identifiers and immediates from the statement, then use the
  # diff to construct the set of identifiers and immediates that were stripped.
  stripped = __tmp4(__tmp7)
  tokens = []

  last_token = []
  last_index = -1
  for i, diff in enumerate(difflib.ndiff(__tmp7, stripped)):
    if diff[0] == "-":
      if i != last_index + 1 and last_token:
        tokens.append("".join(last_token))
        last_token = []

      last_token.append(diff[-1])
      last_index = i

  if last_token:
    tokens.append("".join(last_token))

  return destination.strip(), tokens


def __tmp2(__tmp7) -> typing.Optional[str]:
  """Get the name of a function called in the statement."""
  if "call " not in __tmp7:
    return None
  # Try and resolve the call destination.
  _, m_glob, _, _ = inst2vec_preprocess.get_identifiers_from_line(__tmp7)
  if not m_glob:
    return None
  return m_glob[0][1:]  # strip the leading '@' character


def __tmp6(graph, source_function, __tmp5):
  """Find the statements in function that call another function."""
  call_sites = []
  for node, data in nx_utils.StatementNodeIterator(graph):
    if data["function"] != source_function:
      continue
    called_function = __tmp2(data["text"])
    if not called_function:
      continue
    if called_function == __tmp5:
      call_sites.append(node)
  return call_sites
