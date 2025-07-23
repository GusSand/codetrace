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

    def get_fingerprint(__tmp2, __tmp4, fp_type):
        method_name = 'get_' + fp_type
        method = getattr(__tmp2, method_name)
        if method is None:
            raise Exception(f'{fp_type} is not a supported fingerprint type.')
        return method(__tmp4)

    def get_AP(__tmp2, __tmp4):
        return AllChem.GetAtomPairFingerprint(__tmp4, maxLength=10)

    def get_PHCO(__tmp2, __tmp4):
        return Generate.Gen2DFingerprint(__tmp4, Gobbi_Pharm2D.factory)

    def get_BPF(__tmp2, __tmp4: Mol):
        return GetBPFingerprint(__tmp4)

    def __tmp1(__tmp2, __tmp4):
        return GetBTFingerprint(__tmp4)

    def __tmp3(__tmp2, __tmp4: <FILL>):
        return AllChem.RDKFingerprint(__tmp4)

    def __tmp0(__tmp2, __tmp4):
        return AllChem.GetMorganFingerprint(__tmp4, 2)

    def get_ECFP6(__tmp2, __tmp4):
        return AllChem.GetMorganFingerprint(__tmp4, 3)

    def get_FCFP4(__tmp2, __tmp4: Mol):
        return AllChem.GetMorganFingerprint(__tmp4, 2, useFeatures=True)

    def __tmp5(__tmp2, __tmp4):
        return AllChem.GetMorganFingerprint(__tmp4, 3, useFeatures=True)


def get_fingerprint(__tmp4, fp_type):
    return __typ0().get_fingerprint(__tmp4=__tmp4, fp_type=fp_type)
