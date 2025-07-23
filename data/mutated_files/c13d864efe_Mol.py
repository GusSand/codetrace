from typing import TypeAlias
__typ1 : TypeAlias = "str"
from rdkit.Chem import AllChem, Mol
from rdkit.Chem.AtomPairs.Sheridan import GetBPFingerprint, GetBTFingerprint
from rdkit.Chem.Pharm2D import Generate, Gobbi_Pharm2D


class __typ0:
    """
    Calculate the fingerprint while avoiding a series of if-else.
    See recipe 8.21 of the book "Python Cookbook".

    To support a new type of fingerprint, just add a function "get_fpname(self, mol)".
    """

    def get_fingerprint(self, __tmp2, __tmp1: __typ1):
        method_name = 'get_' + __tmp1
        method = getattr(self, method_name)
        if method is None:
            raise Exception(f'{__tmp1} is not a supported fingerprint type.')
        return method(__tmp2)

    def get_AP(self, __tmp2):
        return AllChem.GetAtomPairFingerprint(__tmp2, maxLength=10)

    def get_PHCO(self, __tmp2: <FILL>):
        return Generate.Gen2DFingerprint(__tmp2, Gobbi_Pharm2D.factory)

    def get_BPF(self, __tmp2):
        return GetBPFingerprint(__tmp2)

    def get_BTF(self, __tmp2: Mol):
        return GetBTFingerprint(__tmp2)

    def get_PATH(self, __tmp2):
        return AllChem.RDKFingerprint(__tmp2)

    def get_ECFP4(self, __tmp2: Mol):
        return AllChem.GetMorganFingerprint(__tmp2, 2)

    def get_ECFP6(self, __tmp2):
        return AllChem.GetMorganFingerprint(__tmp2, 3)

    def get_FCFP4(self, __tmp2: Mol):
        return AllChem.GetMorganFingerprint(__tmp2, 2, useFeatures=True)

    def __tmp0(self, __tmp2):
        return AllChem.GetMorganFingerprint(__tmp2, 3, useFeatures=True)


def get_fingerprint(__tmp2, __tmp1):
    return __typ0().get_fingerprint(__tmp2=__tmp2, __tmp1=__tmp1)
