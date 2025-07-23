
import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K

from typing import Optional

from tensorflow.keras import Model
from tensorflow.keras.layers import Embedding, Lambda, Dropout, BatchNormalization

from rinokeras.core.v1x.common.layers import WeightNormDense as Dense
from rinokeras.core.v1x.common.layers import DenseStack, PositionEmbedding


class __typ0(Model):

    def __init__(__tmp0,
                 embed_size: <FILL>,
                 discrete,
                 n_symbols: Optional[int] = None,
                 dropout: Optional[float] = None,
                 batch_norm: bool = False,
                 n_embed_layers: int = 1,
                 embedding_initializer=None,
                 freeze_embeddings=False,
                 use_position_encoding=True,
                 concat_position_encoding=False,
                 reproject_position_encoding=False,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None) -> None:
        super().__init__()
        __tmp0.embed_size = embed_size
        __tmp0.n_symbols = n_symbols
        __tmp0.n_embed_layers = n_embed_layers
        __tmp0.embedding_initializer = embedding_initializer
        __tmp0.embedding_dense = Lambda(lambda x: x)
        __tmp0.using_dense_embedding = False

        __tmp0.use_position_encoding = use_position_encoding
        __tmp0.concat_position_encoding = concat_position_encoding
        __tmp0.reproject_position_encoding = reproject_position_encoding

        __tmp0.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        __tmp0.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        __tmp0.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)

        if discrete:
            assert n_symbols is not None, 'n_symbols not passed in but model set to discrete'
            assert n_embed_layers == 1, 'discrete models can only have one embedding layer'

            if embedding_initializer is not None:
                assert embedding_initializer.shape[0] == n_symbols, \
                    'n_symbols and initializer shape mismatch'

                if embedding_initializer.shape[1] != embed_size:
                    # We have to correct if the input embedding isn't quite right
                    __tmp0.embedding = Embedding(n_symbols, embedding_initializer.shape[1],
                                               weights=[embedding_initializer],
                                               trainable=not freeze_embeddings)
                    __tmp0.embedding_dense = Dense(embed_size)
                    __tmp0.using_dense_embedding = True
                else:
                    __tmp0.embedding = Embedding(n_symbols, embed_size,
                                               weights=[embedding_initializer])
            else:
                __tmp0.embedding = Embedding(n_symbols, embed_size)
        else:
            assert n_symbols is None, 'n_symbols passed in but model set to continuous'
            assert embedding_initializer is None, 'embedding_initializer passed in but model set to continouous'
            __tmp0.embedding = DenseStack([embed_size] * n_embed_layers, output_activation='relu',
                                        kernel_regularizer=kernel_regularizer,
                                        bias_regularizer=bias_regularizer,
                                        activity_regularizer=activity_regularizer)

        __tmp0.discrete = discrete
        __tmp0.freeze_embeddings = freeze_embeddings
        __tmp0.position_encoding = PositionEmbedding(
            concat=__tmp0.concat_position_encoding, reproject_embedding=reproject_position_encoding)
        __tmp0.dropout_rate = dropout
        __tmp0.dropout = Dropout(0 if dropout is None else dropout)
        __tmp0.use_batch_norm = batch_norm
        __tmp0.batch_norm = None if batch_norm is False else BatchNormalization()

    def __tmp4(__tmp0, __tmp1, start=1):
        # Compute the actual embedding of the inputs by using the embedding layer
        # TODO: Make sure that for non-discrete embeddings, this is handled correctly
        # and allow the shape to be correctly sorted. This should have a tensor
        # as output with shape [batch_size x sequence_len x d_model]
        embedding = __tmp0.embedding(__tmp1)

        if __tmp0.freeze_embeddings:
            embedding = K.stop_gradient(embedding)
        embedding = __tmp0.embedding_dense(embedding)
        embedding = __tmp0.dropout(embedding)

        if __tmp0.batch_norm:
            embedding = __tmp0.batch_norm(embedding)
        if __tmp0.use_position_encoding:
            embedding = __tmp0.position_encoding(embedding, start=start)

        tf.add_to_collection('checkpoints', embedding)

        return embedding

    def __tmp2(__tmp0):
        ei = __tmp0.embedding_initializer.tolist() if __tmp0.embedding_initializer else None
        __tmp3 = {
            'embed_size': __tmp0.embed_size,
            'discrete': __tmp0.discrete,
            'n_symbols': __tmp0.n_symbols,
            'dropout': __tmp0.dropout_rate,
            'batch_norm': __tmp0.use_batch_norm,
            'n_embed_layers': __tmp0.n_embed_layers,
            'embedding_initializer': ei,
            'freeze_embeddings': __tmp0.freeze_embeddings,
            'use_position_encoding': __tmp0.use_position_encoding,
            'concat_position_encoding': __tmp0.concat_position_encoding,
            'reproject_position_encoding': __tmp0.reproject_position_encoding,
            'kernel_regularizer':
            tf.keras.regularizers.serialize(__tmp0.kernel_regularizer),
            'bias_regularizer':
            tf.keras.regularizers.serialize(__tmp0.bias_regularizer),
            'activity_regularizer':
            tf.keras.regularizers.serialize(__tmp0.activity_regularizer)

        }
        return __tmp3

    @classmethod
    def __tmp5(cls, __tmp3):
        ei = __tmp3.pop('embedding_initializer')
        if ei:
            ei = np.array(ei)
        return cls(embedding_initializer=ei, **__tmp3)
