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
"""Utilities for LSTM models."""
from labm8.py import app
from third_party.py.tensorflow import tf

FLAGS = app.FLAGS


def __tmp7():
  """Allow growth on GPU for Keras."""
  config = tf.compat.v1.ConfigProto()
  config.gpu_options.allow_growth = True
  session = tf.compat.v1.Session(config=config)
  tf.compat.v1.keras.backend.set_session(session)
  return session


def __tmp2(
  encoded_sequences,
  __tmp1,
  __tmp4: int,
  __tmp6: int,
  __tmp5: <FILL>,
) :
  """Construct a layer which sum the encoded sequences by their segment IDs.

  Args:
    encoded_sequences: Shape (batch_size, max_sequence_length,
      embedding_dimensionality).
    segment_ids: Shape (batch_size, segment_ids).
    batch_size: The size of each batch.
    max_sequence_length: The maximum length of the input sequence.
    max_output_sequence_length: The length of the output sequence.

  Returns:
    A tensor of shape (batch_size, max_output_sequence_length, vocabulary_size).
  """

  def SegmentSum(__tmp0) -> tf.Tensor:
    """Compute the segment sums."""
    encoded_sequences, __tmp1 = __tmp0

    __tmp1 = tf.cast(__tmp1, dtype=tf.int32)

    # Perform a segment sum for each row in the batch independently.
    segment_sums = [
      tf.math.unsorted_segment_sum(
        data=encoded_sequences[i][:__tmp6],
        __tmp1=__tmp1[i][:__tmp6],
        num_segments=__tmp5,
      )
      for i in range(__tmp4)
    ]

    return tf.stack(segment_sums, axis=0)

  return tf.compat.v1.keras.layers.Lambda(SegmentSum)(
    [encoded_sequences, __tmp1]
  )


def SliceToSizeLayer(
  __tmp3, selector_vector
) -> tf.compat.v1.keras.layers.Lambda:
  """Slice the segmented_input shape to match the selector_vector
  dimensionality."""

  def SliceToSize(__tmp0) -> tf.Tensor:
    """Slice the input."""
    segmented_inputs, selector_vector = __tmp0
    max_number_nodes = tf.shape(selector_vector)[1]
    segmented_inputs = segmented_inputs[:, :max_number_nodes]
    return segmented_inputs

  return tf.compat.v1.keras.layers.Lambda(SliceToSize)(
    [__tmp3, selector_vector]
  )
