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

    def get_fingerprint(__tmp1, __tmp2, __tmp4: __typ0):
        method_name = 'get_' + __tmp4
        method = getattr(__tmp1, method_name)
        if method is None:
            raise Exception(f'{__tmp4} is not a supported fingerprint type.')
        return method(__tmp2)

    def __tmp5(__tmp1, __tmp2: <FILL>):
        return AllChem.GetAtomPairFingerprint(__tmp2, maxLength=10)

    def get_PHCO(__tmp1, __tmp2):
        return Generate.Gen2DFingerprint(__tmp2, Gobbi_Pharm2D.factory)

    def get_BPF(__tmp1, __tmp2):
        return GetBPFingerprint(__tmp2)

    def __tmp0(__tmp1, __tmp2: Mol):
        return GetBTFingerprint(__tmp2)

    def get_PATH(__tmp1, __tmp2):
        return AllChem.RDKFingerprint(__tmp2)

    def get_ECFP4(__tmp1, __tmp2):
        return AllChem.GetMorganFingerprint(__tmp2, 2)

    def __tmp3(__tmp1, __tmp2):
        return AllChem.GetMorganFingerprint(__tmp2, 3)

    def get_FCFP4(__tmp1, __tmp2):
        return AllChem.GetMorganFingerprint(__tmp2, 2, useFeatures=True)

    def get_FCFP6(__tmp1, __tmp2: Mol):
        return AllChem.GetMorganFingerprint(__tmp2, 3, useFeatures=True)


def get_fingerprint(__tmp2, __tmp4: __typ0):
    return _FingerprintCalculator().get_fingerprint(__tmp2=__tmp2, __tmp4=__tmp4)
