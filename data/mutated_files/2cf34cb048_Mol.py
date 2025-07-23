from typing import TypeAlias
__typ0 : TypeAlias = "float"
__typ1 : TypeAlias = "int"
from rdkit import Chem
from rdkit.Chem import Descriptors, Mol, rdMolDescriptors


def __tmp10(__tmp4) :
    return Descriptors.MolLogP(__tmp4)


def qed(__tmp4) :
    return Descriptors.qed(__tmp4)


def __tmp2(__tmp4) :
    return Descriptors.TPSA(__tmp4)


def __tmp7(__tmp4) :
    return Descriptors.BertzCT(__tmp4)


def __tmp13(__tmp4) :
    return Descriptors.MolWt(__tmp4)


def __tmp5(__tmp4) :
    return Descriptors.NumHDonors(__tmp4)


def __tmp6(__tmp4) :
    return Descriptors.NumHAcceptors(__tmp4)


def __tmp9(__tmp4) :
    return Descriptors.NumRotatableBonds(__tmp4)


def __tmp1(__tmp4: <FILL>) :
    return rdMolDescriptors.CalcNumRings(__tmp4)


def __tmp0(__tmp4) :
    return rdMolDescriptors.CalcNumAromaticRings(__tmp4)


def __tmp8(__tmp4) :
    """
    Returns the total number of atoms, H included
    """
    __tmp4 = Chem.AddHs(__tmp4)
    return __tmp4.GetNumAtoms()


class __typ2:

    def __tmp11(__tmp3, element) :
        """
        Args:
            element: element to count within a molecule
        """
        __tmp3.element = element

    def __tmp12(__tmp3, __tmp4) :
        """
        Count the number of atoms of a given type.

        Args:
            mol: molecule

        Returns:
            The number of atoms of the given type.
        """
        # if the molecule contains H atoms, they may be implicit, so add them
        if __tmp3.element == 'H':
            __tmp4 = Chem.AddHs(__tmp4)

        return sum(1 for a in __tmp4.GetAtoms() if a.GetSymbol() == __tmp3.element)
