
from typing import Optional
import torch

from rinokeras.core.torch.functional.similarity import scaled_dot_product_similarity
from rinokeras.core.torch.functional.masking import apply_attention_mask


ATTENTION_METHODS_MAP = {
    'scaled_dot': scaled_dot_product_similarity
}
ATTENTION_FUNCTION_MAP = {
    'softmax': torch.nn.functional.softmax,
}

def attention_map(__tmp1: torch.Tensor,
                  __tmp2: torch.Tensor,
                  values: torch.Tensor,
                  mask: torch.Tensor = None,
                  dropout: Optional[float] = None,
                  return_attention_weights: bool = True,
                  similarity_metric: str = 'scaled_dot',
                  attention_function: str = 'softmax') -> torch.Tensor:

    similarity = ATTENTION_METHODS_MAP[similarity_metric](__tmp1, __tmp2)

    if attention_function == 'softmax':
        masked_similarity = apply_attention_mask(similarity, mask=mask)
        weights = torch.nn.functional.softmax(masked_similarity - torch.max(masked_similarity, dim=-1, keepdim=True)[0], dim=-1)
    else:
        masked_similarity = apply_attention_mask(similarity, mask=mask, hadamard=True)
        weights = ATTENTION_FUNCTION_MAP[attention_function](masked_similarity, dim=-1)

    if dropout:
        weights = torch.nn.functional.dropout(weights, dropout)
    outputs = torch.matmul(weights, values)
    if return_attention_weights:
        return outputs, weights
    return outputs

def __tmp0(__tmp5, __tmp3:<FILL>) -> torch.Tensor:
    # Splits the last dimension into a heads dimension
    if __tmp5.shape[-1] % __tmp3 != 0:
        raise AssertionError('Tensor shape at dimension -1 ({}) must be divisible by n_heads ({})'.format(__tmp5.shape[-1], __tmp3))
    if len(__tmp5.shape) != 3:
        raise AssertionError('Input to split_heads must be rank 3')
    
    output = __tmp5.reshape(__tmp5.shape[0], __tmp5.shape[1], __tmp3, __tmp5.shape[2]//__tmp3)
    return output.permute(0,2,1,3)

def __tmp6(__tmp5: torch.Tensor) -> torch.Tensor:
    if len(__tmp5.shape) != 4:
        raise AssertionError('Input to combine_heads must be rank 4')
    output = __tmp5.permute(0,2,1,3)
    return output.reshape(__tmp5.shape[0], __tmp5.shape[2], -1)

def __tmp4(__tmp1: torch.Tensor,
                             __tmp2: torch.Tensor,
                             values: torch.Tensor,
                             __tmp3: int,
                             mask: torch.Tensor = None,
                             dropout: Optional[float] = None,
                             return_attention_weights: bool = True,
                             similarity_metric: str = 'scaled_dot',
                             attention_function: str = 'softmax') :

    queries_split = __tmp0(__tmp1, __tmp3)
    keys_split = __tmp0(__tmp2, __tmp3)
    values_split = __tmp0(values, __tmp3)

    attention_outputs, attention_weights = attention_map(__tmp1=queries_split,
                                                        __tmp2=keys_split,
                                                        values=values_split,
                                                        mask=mask,
                                                        dropout=dropout,
                                                        return_attention_weights=True,
                                                        similarity_metric=similarity_metric,
                                                        attention_function=attention_function)

    outputs = __tmp6(attention_outputs)

    if return_attention_weights:
        return outputs, attention_weights
    return outputs
