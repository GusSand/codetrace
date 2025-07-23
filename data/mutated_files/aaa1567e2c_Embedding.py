"""

Invertible layers, such as the InvertibleDense layer and the DenseTranspose
layers.

"""
import numpy as np
import scipy

import tensorflow as tf
from tensorflow.python.eager import context
from tensorflow.python.framework import common_shapes
from tensorflow.python.framework import ops
from tensorflow.python.ops import standard_ops
from tensorflow.python.ops import gen_math_ops
from tensorflow.keras import Model  # pylint: disable=F0401
from tensorflow.keras.layers import Layer, Dense, Embedding   # pylint: disable=F0401
import tensorflow.keras.backend as K  # pylint: disable=F0401



class DenseTranspose(Layer):
    """Multiply by the transpose of a dense layer
    """
    def __init__(__tmp0, other_layer):
        super(DenseTranspose, __tmp0).__init__()
        __tmp0.other_layer = other_layer

    def __tmp2(__tmp0, x):
        return K.dot(x - K.stop_gradient(__tmp0.other_layer.bias), K.transpose(K.stop_gradient(__tmp0.other_layer.kernel)))


class EmbeddingTranspose(Model):
    """Multiply by the transpose of an embedding layer
    """
    def __init__(__tmp0, __tmp4: <FILL>, *args, **kwargs) :
        super(EmbeddingTranspose, __tmp0).__init__(*args, **kwargs)
        __tmp0.embedding = __tmp4

    def __tmp2(__tmp0, __tmp1):
        embed_mat = __tmp0.embedding.weights[0]
        return K.dot(__tmp1, K.stop_gradient(K.transpose(embed_mat)))


class __typ0(Dense):

    def __init__(__tmp0, *args, **kwargs):
        super().__init__(*args, use_bias=False, kernel_initializer=None, activation=None, **kwargs)

    def build(__tmp0, __tmp3):
        assert __tmp3[-1] == __tmp0.units, \
            'Cannot create invertible layer when mapping from {} to {} dimensions'.format(
                __tmp3[-1].value, __tmp0.units)
        H = np.random.randn(__tmp3[-1].value, __tmp0.units)
        Q, _ = scipy.linalg.qr(H)
        if np.linalg.det(Q) < 0:
            Q[:, 0] *= -1
        initializer = tf.keras.initializers.Constant(Q)

        __tmp0.kernel_initializer = initializer
        super().build(__tmp3)
        __tmp0.kernel_inverse = tf.linalg.inv(__tmp0.kernel)

    def __tmp2(__tmp0, __tmp1, reverse=False):
        __tmp1 = ops.convert_to_tensor(__tmp1, dtype=__tmp0.dtype)
        rank = common_shapes.rank(__tmp1)

        kernel = __tmp0.kernel if not reverse else __tmp0.kernel_inverse

        if rank > 2:
            # Broadcasting is required for the inputs.
            outputs = standard_ops.tensordot(__tmp1, kernel, [[rank - 1], [0]])
            if not context.executing_eagerly():
                shape = __tmp1.get_shape().as_list()
                output_shape = shape[:-1] + [__tmp0.units]
                outputs.set_shape(output_shape)
        else:
            outputs = gen_math_ops.mat_mul(__tmp1, kernel)

        if reverse:
            return outputs

        batch_size = tf.cast(tf.shape(__tmp1)[0], tf.float32)
        sequence_length = tf.cast(tf.shape(__tmp1)[1], tf.float32)
        # tf.logdet only works on Hermitian positive def matrices, maybe try tf.slogdet?
        log_det_W = batch_size * sequence_length * tf.log(tf.linalg.det(__tmp0.kernel))
        return outputs, log_det_W
