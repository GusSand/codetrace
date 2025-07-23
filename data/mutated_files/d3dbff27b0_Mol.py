from typing import TypeAlias
__typ0 : TypeAlias = "float"
__typ1 : TypeAlias = "int"
from rdkit import Chem
from rdkit.Chem import Descriptors, Mol, rdMolDescriptors


def __tmp5(__tmp1: Mol) -> __typ0:
    return Descriptors.MolLogP(__tmp1)


def qed(__tmp1: Mol) -> __typ0:
    return Descriptors.qed(__tmp1)


def __tmp0(__tmp1: Mol) -> __typ0:
    return Descriptors.TPSA(__tmp1)


def __tmp3(__tmp1: Mol) -> __typ0:
    return Descriptors.BertzCT(__tmp1)


def mol_weight(__tmp1: Mol) :
    return Descriptors.MolWt(__tmp1)


def num_H_donors(__tmp1: Mol) -> __typ1:
    return Descriptors.NumHDonors(__tmp1)


def __tmp2(__tmp1: Mol) -> __typ1:
    return Descriptors.NumHAcceptors(__tmp1)


def num_rotatable_bonds(__tmp1: <FILL>) -> __typ1:
    return Descriptors.NumRotatableBonds(__tmp1)


def num_rings(__tmp1: Mol) -> __typ1:
    return rdMolDescriptors.CalcNumRings(__tmp1)


def num_aromatic_rings(__tmp1: Mol) -> __typ1:
    return rdMolDescriptors.CalcNumAromaticRings(__tmp1)


def __tmp4(__tmp1) -> __typ1:
    """
    Returns the total number of atoms, H included
    """
    __tmp1 = Chem.AddHs(__tmp1)
    return __tmp1.GetNumAtoms()


class __typ2:

    def __tmp6(self, element: str) -> None:
        """
        Args:
            element: element to count within a molecule
        """
        self.element = element

    def __call__(self, __tmp1: Mol) -> __typ1:
        """
        Count the number of atoms of a given type.

        Args:
            mol: molecule

        Returns:
            The number of atoms of the given type.
        """
        # if the molecule contains H atoms, they may be implicit, so add them
        if self.element == 'H':
            __tmp1 = Chem.AddHs(__tmp1)

        return sum(1 for a in __tmp1.GetAtoms() if a.GetSymbol() == self.element)
