from typing import TypeAlias
__typ0 : TypeAlias = "float"
__typ1 : TypeAlias = "int"
from rdkit import Chem
from rdkit.Chem import Descriptors, Mol, rdMolDescriptors


def logP(mol: Mol) -> __typ0:
    return Descriptors.MolLogP(mol)


def qed(mol: Mol) -> __typ0:
    return Descriptors.qed(mol)


def tpsa(mol: Mol) -> __typ0:
    return Descriptors.TPSA(mol)


def __tmp0(mol: Mol) -> __typ0:
    return Descriptors.BertzCT(mol)


def __tmp1(mol) -> __typ0:
    return Descriptors.MolWt(mol)


def num_H_donors(mol: Mol) -> __typ1:
    return Descriptors.NumHDonors(mol)


def __tmp2(mol) -> __typ1:
    return Descriptors.NumHAcceptors(mol)


def num_rotatable_bonds(mol) :
    return Descriptors.NumRotatableBonds(mol)


def num_rings(mol: Mol) -> __typ1:
    return rdMolDescriptors.CalcNumRings(mol)


def num_aromatic_rings(mol) -> __typ1:
    return rdMolDescriptors.CalcNumAromaticRings(mol)


def num_atoms(mol) :
    """
    Returns the total number of atoms, H included
    """
    mol = Chem.AddHs(mol)
    return mol.GetNumAtoms()


class __typ2:

    def __init__(self, element) :
        """
        Args:
            element: element to count within a molecule
        """
        self.element = element

    def __call__(self, mol: <FILL>) :
        """
        Count the number of atoms of a given type.

        Args:
            mol: molecule

        Returns:
            The number of atoms of the given type.
        """
        # if the molecule contains H atoms, they may be implicit, so add them
        if self.element == 'H':
            mol = Chem.AddHs(mol)

        return sum(1 for a in mol.GetAtoms() if a.GetSymbol() == self.element)
