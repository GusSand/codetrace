from typing import TypeAlias
__typ2 : TypeAlias = "float"
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
from rdkit import Chem
from rdkit.Chem import Descriptors, Mol, rdMolDescriptors


def __tmp9(__tmp3) :
    return Descriptors.MolLogP(__tmp3)


def qed(__tmp3) :
    return Descriptors.qed(__tmp3)


def tpsa(__tmp3: <FILL>) :
    return Descriptors.TPSA(__tmp3)


def __tmp5(__tmp3) :
    return Descriptors.BertzCT(__tmp3)


def __tmp12(__tmp3) :
    return Descriptors.MolWt(__tmp3)


def __tmp4(__tmp3) :
    return Descriptors.NumHDonors(__tmp3)


def __tmp6(__tmp3) :
    return Descriptors.NumHAcceptors(__tmp3)


def __tmp8(__tmp3) :
    return Descriptors.NumRotatableBonds(__tmp3)


def __tmp1(__tmp3) :
    return rdMolDescriptors.CalcNumRings(__tmp3)


def __tmp0(__tmp3) :
    return rdMolDescriptors.CalcNumAromaticRings(__tmp3)


def __tmp7(__tmp3) :
    """
    Returns the total number of atoms, H included
    """
    __tmp3 = Chem.AddHs(__tmp3)
    return __tmp3.GetNumAtoms()


class __typ3:

    def __tmp11(__tmp2, element) :
        """
        Args:
            element: element to count within a molecule
        """
        __tmp2.element = element

    def __tmp10(__tmp2, __tmp3) :
        """
        Count the number of atoms of a given type.

        Args:
            mol: molecule

        Returns:
            The number of atoms of the given type.
        """
        # if the molecule contains H atoms, they may be implicit, so add them
        if __tmp2.element == 'H':
            __tmp3 = Chem.AddHs(__tmp3)

        return sum(1 for a in __tmp3.GetAtoms() if a.GetSymbol() == __tmp2.element)
