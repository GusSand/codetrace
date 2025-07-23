from typing import TypeAlias
__typ0 : TypeAlias = "float"
__typ2 : TypeAlias = "Mol"
__typ1 : TypeAlias = "int"
from rdkit import Chem
from rdkit.Chem import Descriptors, Mol, rdMolDescriptors


def logP(__tmp3) -> __typ0:
    return Descriptors.MolLogP(__tmp3)


def qed(__tmp3: __typ2) -> __typ0:
    return Descriptors.qed(__tmp3)


def tpsa(__tmp3) -> __typ0:
    return Descriptors.TPSA(__tmp3)


def bertz(__tmp3: __typ2) :
    return Descriptors.BertzCT(__tmp3)


def __tmp2(__tmp3: __typ2) :
    return Descriptors.MolWt(__tmp3)


def num_H_donors(__tmp3: __typ2) :
    return Descriptors.NumHDonors(__tmp3)


def num_H_acceptors(__tmp3) -> __typ1:
    return Descriptors.NumHAcceptors(__tmp3)


def num_rotatable_bonds(__tmp3: __typ2) -> __typ1:
    return Descriptors.NumRotatableBonds(__tmp3)


def __tmp0(__tmp3: __typ2) -> __typ1:
    return rdMolDescriptors.CalcNumRings(__tmp3)


def num_aromatic_rings(__tmp3: __typ2) -> __typ1:
    return rdMolDescriptors.CalcNumAromaticRings(__tmp3)


def num_atoms(__tmp3: __typ2) :
    """
    Returns the total number of atoms, H included
    """
    __tmp3 = Chem.AddHs(__tmp3)
    return __tmp3.GetNumAtoms()


class AtomCounter:

    def __init__(self, element: <FILL>) :
        """
        Args:
            element: element to count within a molecule
        """
        self.element = element

    def __tmp1(self, __tmp3) :
        """
        Count the number of atoms of a given type.

        Args:
            mol: molecule

        Returns:
            The number of atoms of the given type.
        """
        # if the molecule contains H atoms, they may be implicit, so add them
        if self.element == 'H':
            __tmp3 = Chem.AddHs(__tmp3)

        return sum(1 for a in __tmp3.GetAtoms() if a.GetSymbol() == self.element)
