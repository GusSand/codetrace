import torch

class __typ0(torch.nn.Module):
    def __init__(__tmp0, input_units: <FILL>, output_units):
        """
        Gated TanH activation layer from https://arxiv.org/pdf/1612.08083.pdf
        
        Arguments:
            input_units {int} -- The number of input units to the module
            output_units {int} -- The numer of output units from the module
        """
        super(__typ0, __tmp0).__init__()
        __tmp0.input_units = input_units
        __tmp0.output_units = output_units

        # The linear input and output gates
        __tmp0.linear_forward = torch.nn.Linear(__tmp0.input_units, __tmp0.output_units, bias=True)
        __tmp0.gate = torch.nn.Linear(__tmp0.input_units, __tmp0.output_units, bias=True)

    def __tmp1(__tmp0, *inputs):
        forward_out = torch.nn.functional.tanh(__tmp0.linear_forward(*inputs))
        gate_out = torch.nn.functional.sigmoid(__tmp0.gate(*inputs))
        return forward_out * gate_out