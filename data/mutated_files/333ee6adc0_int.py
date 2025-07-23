from typing import TypeAlias
__typ0 : TypeAlias = "float"
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


class __typ1(cirq.ops.Qid):
    """A qubit in 3d.

    ThreeDQubits use z-y-x ordering:

        ThreeDQubit(0, 0, 0) < ThreeDQubit(1, 0, 0)
        < ThreeDQubit(0, 1, 0) < ThreeDQubit(1, 1, 0)
        < ThreeDQubit(0, 0, 1) < ThreeDQubit(1, 0, 1)
        < ThreeDQubit(0, 1, 1) < ThreeDQubit(1, 1, 1)
    """

    def __init__(__tmp1, x, y, z: __typ0):
        __tmp1.x = x
        __tmp1.y = y
        __tmp1.z = z

    def _comparison_key(__tmp1):
        return round(__tmp1.z, 15), round(__tmp1.y, 15), round(__tmp1.x, 15)

    @property
    def dimension(__tmp1) :
        return 2

    def distance(__tmp1, other: cirq.ops.Qid) -> __typ0:
        """Returns the distance between two qubits in 3d."""
        if not isinstance(other, __typ1):
            raise TypeError(f"Can compute distance to another ThreeDQubit, but {other}")
        return sqrt((__tmp1.x - other.x) ** 2 + (__tmp1.y - other.y) ** 2 + (__tmp1.z - other.z) ** 2)

    @staticmethod
    def cube(diameter: int, x0: __typ0 = 0, y0: __typ0 = 0, z0: __typ0 = 0) :
        """Returns a cube of ThreeDQubits.

        Args:
            diameter: Length of a side of the square.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit
            z0: z-coordinate of the first qubit.

        Returns:
            A list of ThreeDQubits filling in a square grid
        """
        return __typ1.parallelep(diameter, diameter, diameter, x0=x0, y0=y0, z0=z0)

    @staticmethod
    def parallelep(
        rows, cols: int, lays: int, x0: __typ0 = 0, y0: __typ0 = 0, z0: __typ0 = 0
    ) :
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
            __typ1(x0 + x, y0 + y, z0 + z)
            for z in range(lays)
            for y in range(cols)
            for x in range(rows)
        ]

    def __repr__(__tmp1):
        return f'pasqal.ThreeDQubit({__tmp1.x}, {__tmp1.y}, {__tmp1.z})'

    def __str__(__tmp1):
        return f'({__tmp1.x}, {__tmp1.y}, {__tmp1.z})'

    def _json_dict_(__tmp1):
        return cirq.protocols.obj_to_dict_helper(__tmp1, ['x', 'y', 'z'])


class __typ2(__typ1):
    """A qubit in 2d."""

    def __init__(__tmp1, x: __typ0, y):
        super().__init__(x, y, z=0)

    @staticmethod
    def square(diameter: <FILL>, x0: __typ0 = 0, y0: __typ0 = 0) -> List['TwoDQubit']:
        """Returns a square of TwoDQubit.

        Args:
            diameter: Length of a side of the square.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit.

        Returns:
            A list of TwoDQubits filling in a square grid
        """
        return __typ2.rect(diameter, diameter, x0=x0, y0=y0)

    @staticmethod
    def rect(rows: int, cols: int, x0: __typ0 = 0, y0: __typ0 = 0) -> List['TwoDQubit']:
        """Returns a rectangle of TwoDQubit.

        Args:
            rows: Number of rows in the rectangle.
            cols: Number of columns in the rectangle.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit.

        Returns:
            A list of TwoDQubits filling in a rectangular grid
        """
        return [__typ2(x0 + x, y0 + y) for y in range(cols) for x in range(rows)]

    @staticmethod
    def __tmp0(l, x0: __typ0 = 0, y0: __typ0 = 0):
        """Returns a triangular lattice of TwoDQubits.

        Args:
            l: Number of qubits along one direction.
            x0: x-coordinate of the first qubit.
            y0: y-coordinate of the first qubit.

        Returns:
            A list of TwoDQubits filling in a triangular lattice.
        """
        coords = np.array([[x, y] for x in range(l + 1) for y in range(l + 1)], dtype=__typ0)
        coords[:, 0] += 0.5 * np.mod(coords[:, 1], 2)
        coords[:, 1] *= np.sqrt(3) / 2
        coords += [x0, y0]

        return [__typ2(coord[0], coord[1]) for coord in coords]

    def __repr__(__tmp1):
        return f'pasqal.TwoDQubit({__tmp1.x}, {__tmp1.y})'

    def __str__(__tmp1):
        return f'({__tmp1.x}, {__tmp1.y})'

    def _json_dict_(__tmp1):
        return cirq.protocols.obj_to_dict_helper(__tmp1, ['x', 'y'])
