from typing import TypeAlias
__typ1 : TypeAlias = "int"
# Copyright 2020 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List
from numpy import sqrt
import numpy as np

import cirq


class __typ0(cirq.ops.Qid):
    """A qubit in 3d.

    ThreeDQubits use z-y-x ordering:

        ThreeDQubit(0, 0, 0) < ThreeDQubit(1, 0, 0)
        < ThreeDQubit(0, 1, 0) < ThreeDQubit(1, 1, 0)
        < ThreeDQubit(0, 0, 1) < ThreeDQubit(1, 0, 1)
        < ThreeDQubit(0, 1, 1) < ThreeDQubit(1, 1, 1)
    """

    def __init__(__tmp1, x, y, z: float):
        __tmp1.x = x
        __tmp1.y = y
        __tmp1.z = z

    def __tmp5(__tmp1):
        return round(__tmp1.z, 15), round(__tmp1.y, 15), round(__tmp1.x, 15)

    @property
    def __tmp4(__tmp1) :
        return 2

    def __tmp2(__tmp1, __tmp7) :
        """Returns the distance between two qubits in 3d."""
        if not isinstance(__tmp7, __typ0):
            raise TypeError(f"Can compute distance to another ThreeDQubit, but {__tmp7}")
        return sqrt((__tmp1.x - __tmp7.x) ** 2 + (__tmp1.y - __tmp7.y) ** 2 + (__tmp1.z - __tmp7.z) ** 2)

    @staticmethod
    def __tmp6(__tmp8, x0: float = 0, y0: float = 0, z0: float = 0) -> List['ThreeDQubit']:
        """Returns a cube of ThreeDQubits.

        Args:
            diameter: Length of a side of the square.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit
            z0: z-coordinate of the first qubit.

        Returns:
            A list of ThreeDQubits filling in a square grid
        """
        return __typ0.parallelep(__tmp8, __tmp8, __tmp8, x0=x0, y0=y0, z0=z0)

    @staticmethod
    def parallelep(
        __tmp0, __tmp9: __typ1, lays, x0: float = 0, y0: float = 0, z0: float = 0
    ) -> List['ThreeDQubit']:
        """Returns a parallelepiped of ThreeDQubits.

        Args:
            rows: Number of rows in the parallelepiped.
            cols: Number of columns in the parallelepiped.
            lays: Number of layers in the parallelepiped.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit.
            z0: z-coordinate of the first qubit.

        Returns:
            A list of ThreeDQubits filling in a 3d grid
        """
        return [
            __typ0(x0 + x, y0 + y, z0 + z)
            for z in range(lays)
            for y in range(__tmp9)
            for x in range(__tmp0)
        ]

    def __tmp10(__tmp1):
        return f'pasqal.ThreeDQubit({__tmp1.x}, {__tmp1.y}, {__tmp1.z})'

    def __tmp13(__tmp1):
        return f'({__tmp1.x}, {__tmp1.y}, {__tmp1.z})'

    def __tmp11(__tmp1):
        return cirq.protocols.obj_to_dict_helper(__tmp1, ['x', 'y', 'z'])


class TwoDQubit(__typ0):
    """A qubit in 2d."""

    def __init__(__tmp1, x: <FILL>, y):
        super().__init__(x, y, z=0)

    @staticmethod
    def __tmp14(__tmp8, x0: float = 0, y0: float = 0) :
        """Returns a square of TwoDQubit.

        Args:
            diameter: Length of a side of the square.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit.

        Returns:
            A list of TwoDQubits filling in a square grid
        """
        return TwoDQubit.rect(__tmp8, __tmp8, x0=x0, y0=y0)

    @staticmethod
    def rect(__tmp0, __tmp9, x0: float = 0, y0: float = 0) :
        """Returns a rectangle of TwoDQubit.

        Args:
            rows: Number of rows in the rectangle.
            cols: Number of columns in the rectangle.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit.

        Returns:
            A list of TwoDQubits filling in a rectangular grid
        """
        return [TwoDQubit(x0 + x, y0 + y) for y in range(__tmp9) for x in range(__tmp0)]

    @staticmethod
    def __tmp12(__tmp3, x0: float = 0, y0: float = 0):
        """Returns a triangular lattice of TwoDQubits.

        Args:
            l: Number of qubits along one direction.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit.

        Returns:
            A list of TwoDQubits filling in a triangular lattice.
        """
        coords = np.array([[x, y] for x in range(__tmp3 + 1) for y in range(__tmp3 + 1)], dtype=float)
        coords[:, 0] += 0.5 * np.mod(coords[:, 1], 2)
        coords[:, 1] *= np.sqrt(3) / 2
        coords += [x0, y0]

        return [TwoDQubit(coord[0], coord[1]) for coord in coords]

    def __tmp10(__tmp1):
        return f'pasqal.TwoDQubit({__tmp1.x}, {__tmp1.y})'

    def __tmp13(__tmp1):
        return f'({__tmp1.x}, {__tmp1.y})'

    def __tmp11(__tmp1):
        return cirq.protocols.obj_to_dict_helper(__tmp1, ['x', 'y'])
