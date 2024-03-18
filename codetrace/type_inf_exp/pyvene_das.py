"""
Taken from pyvene: https://github.com/stanfordnlp/pyvene/tree/main
"""

import torch

class RotateLayer(torch.nn.Module):
    """A linear transformation with orthogonal initialization."""

    def __init__(self, n, init_orth=True):
        super().__init__()
        weight = torch.empty(n, n)
        # we don't need init if the saved checkpoint has a nice
        # starting point already.
        # you can also study this if you want, but it is our focus.
        if init_orth:
            torch.nn.init.orthogonal_(weight)
        self.weight = torch.nn.Parameter(weight, requires_grad=True)

    def forward(self, x):
        return torch.matmul(x.to(self.weight.dtype), self.weight)

def sigmoid_boundary(_input, boundary_x, boundary_y, temperature):
    """Generate sigmoid mask"""
    return torch.sigmoid((_input - boundary_x) / temperature) * torch.sigmoid(
        (boundary_y - _input) / temperature
    )


class BoundlessRotatedSpaceIntervention(torch.nn.Module):

    """Intervention in the rotated space with boundary mask."""

    def __init__(self, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        rotate_layer = RotateLayer(embed_dim)
        self.rotate_layer = torch.nn.utils.parametrizations.orthogonal(rotate_layer)
        self.intervention_boundaries = torch.nn.Parameter(
            torch.tensor([0.5]), requires_grad=True
        )
        self.temperature = torch.nn.Parameter(torch.tensor(50.0))
        self.intervention_population = torch.nn.Parameter(
            torch.arange(0, self.embed_dim), requires_grad=False
        )

    def get_boundary_parameters(self):
        return self.intervention_boundaries

    def get_temperature(self):
        return self.temperature

    def set_temperature(self, temp: torch.Tensor):
        self.temperature.data = temp

    def set_intervention_boundaries(self, intervention_boundaries):
        self.intervention_boundaries = torch.nn.Parameter(
            torch.tensor([intervention_boundaries]), requires_grad=True
        )
        
    def forward(self, base, source, subspaces=None):
        batch_size = base.shape[0]
        rotated_base = self.rotate_layer(base)
        rotated_source = self.rotate_layer(source)
        # get boundary
        intervention_boundaries = torch.clamp(self.intervention_boundaries, 1e-3, 1)
        boundary_mask = sigmoid_boundary(
            self.intervention_population.repeat(batch_size, 1),
            0.0,
            intervention_boundaries[0] * int(self.embed_dim),
            self.temperature,
        )
        boundary_mask = (
            torch.ones(batch_size, device=source.device).unsqueeze(dim=-1) * boundary_mask
        )
        boundary_mask = boundary_mask.to(rotated_base.dtype)
        # interchange
        rotated_output = (
            1.0 - boundary_mask
        ) * rotated_base + boundary_mask * rotated_source
        # inverse output
        output = torch.matmul(rotated_output, self.rotate_layer.weight.T)
        return output.to(base.dtype)

    def __str__(self):
        return f"BoundlessRotatedSpaceIntervention()"