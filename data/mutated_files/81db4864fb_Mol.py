from typing import TypeAlias
__typ0 : TypeAlias = "str"
from rdkit.Chem import AllChem, Mol
from rdkit.Chem.AtomPairs.Sheridan import GetBPFingerprint, GetBTFingerprint
from rdkit.Chem.Pharm2D import Generate, Gobbi_Pharm2D


class _FingerprintCalculator:
    """
    Calculate the fingerprint while avoiding a series of if-else.
    See recipe 8.21 of the book "Python Cookbook".

    To support a new type of fingerprint, just add a function "get_fpname(self, mol)".
    """

    def get_fingerprint(__tmp2, __tmp5: Mol, fp_type):
        method_name = 'get_' + fp_type
        method = getattr(__tmp2, method_name)
        if method is None:
            raise Exception(f'{fp_type} is not a supported fingerprint type.')
        return method(__tmp5)

    def __tmp7(__tmp2, __tmp5):
        return AllChem.GetAtomPairFingerprint(__tmp5, maxLength=10)

    def get_PHCO(__tmp2, __tmp5):
        return Generate.Gen2DFingerprint(__tmp5, Gobbi_Pharm2D.factory)

    def __tmp6(__tmp2, __tmp5: Mol):
        return GetBPFingerprint(__tmp5)

    def __tmp1(__tmp2, __tmp5: <FILL>):
        return GetBTFingerprint(__tmp5)

    def __tmp4(__tmp2, __tmp5: Mol):
        return AllChem.RDKFingerprint(__tmp5)

    def __tmp0(__tmp2, __tmp5: Mol):
        return AllChem.GetMorganFingerprint(__tmp5, 2)

    def get_ECFP6(__tmp2, __tmp5: Mol):
        return AllChem.GetMorganFingerprint(__tmp5, 3)

    def __tmp3(__tmp2, __tmp5: Mol):
        return AllChem.GetMorganFingerprint(__tmp5, 2, useFeatures=True)

    def __tmp8(__tmp2, __tmp5: Mol):
        return AllChem.GetMorganFingerprint(__tmp5, 3, useFeatures=True)


def get_fingerprint(__tmp5: Mol, fp_type):
    return _FingerprintCalculator().get_fingerprint(__tmp5=__tmp5, fp_type=fp_type)
