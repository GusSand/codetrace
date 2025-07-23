from typing import TypeAlias
__typ0 : TypeAlias = "float"
__typ3 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
from rdkit import Chem
from rdkit.Chem import Descriptors, Mol, rdMolDescriptors


def __tmp6(__tmp2: Mol) -> __typ0:
    return Descriptors.MolLogP(__tmp2)


def qed(__tmp2) :
    return Descriptors.qed(__tmp2)


def __tmp0(__tmp2: Mol) -> __typ0:
    return Descriptors.TPSA(__tmp2)


def __tmp4(__tmp2: Mol) :
    return Descriptors.BertzCT(__tmp2)


def mol_weight(__tmp2) :
    return Descriptors.MolWt(__tmp2)


def __tmp3(__tmp2) :
    return Descriptors.NumHDonors(__tmp2)


def num_H_acceptors(__tmp2) :
    return Descriptors.NumHAcceptors(__tmp2)


def __tmp5(__tmp2) -> __typ1:
    return Descriptors.NumRotatableBonds(__tmp2)


def num_rings(__tmp2) :
    return rdMolDescriptors.CalcNumRings(__tmp2)


def num_aromatic_rings(__tmp2: <FILL>) :
    return rdMolDescriptors.CalcNumAromaticRings(__tmp2)


def num_atoms(__tmp2) :
    """
    Returns the total number of atoms, H included
    """
    __tmp2 = Chem.AddHs(__tmp2)
    return __tmp2.GetNumAtoms()


class __typ2:

    def __init__(__tmp1, element) -> None:
        """
        Args:
            element: element to count within a molecule
        """
        __tmp1.element = element

    def __call__(__tmp1, __tmp2) :
        """
        Count the number of atoms of a given type.

        Args:
            mol: molecule

        Returns:
            The number of atoms of the given type.
        """
        # if the molecule contains H atoms, they may be implicit, so add them
        if __tmp1.element == 'H':
            __tmp2 = Chem.AddHs(__tmp2)

        return sum(1 for a in __tmp2.GetAtoms() if a.GetSymbol() == __tmp1.element)
