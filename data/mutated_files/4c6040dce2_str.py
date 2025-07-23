from typing import TypeAlias
__typ1 : TypeAlias = "Mol"
from rdkit.Chem import AllChem, Mol
from rdkit.Chem.AtomPairs.Sheridan import GetBPFingerprint, GetBTFingerprint
from rdkit.Chem.Pharm2D import Generate, Gobbi_Pharm2D


class __typ0:
    """
    Calculate the fingerprint while avoiding a series of if-else.
    See recipe 8.21 of the book "Python Cookbook".

    To support a new type of fingerprint, just add a function "get_fpname(self, mol)".
    """

    def get_fingerprint(__tmp1, __tmp2: __typ1, fp_type: <FILL>):
        method_name = 'get_' + fp_type
        method = getattr(__tmp1, method_name)
        if method is None:
            raise Exception(f'{fp_type} is not a supported fingerprint type.')
        return method(__tmp2)

    def get_AP(__tmp1, __tmp2):
        return AllChem.GetAtomPairFingerprint(__tmp2, maxLength=10)

    def get_PHCO(__tmp1, __tmp2: __typ1):
        return Generate.Gen2DFingerprint(__tmp2, Gobbi_Pharm2D.factory)

    def get_BPF(__tmp1, __tmp2: __typ1):
        return GetBPFingerprint(__tmp2)

    def get_BTF(__tmp1, __tmp2):
        return GetBTFingerprint(__tmp2)

    def get_PATH(__tmp1, __tmp2):
        return AllChem.RDKFingerprint(__tmp2)

    def __tmp0(__tmp1, __tmp2):
        return AllChem.GetMorganFingerprint(__tmp2, 2)

    def __tmp3(__tmp1, __tmp2: __typ1):
        return AllChem.GetMorganFingerprint(__tmp2, 3)

    def __tmp4(__tmp1, __tmp2: __typ1):
        return AllChem.GetMorganFingerprint(__tmp2, 2, useFeatures=True)

    def get_FCFP6(__tmp1, __tmp2: __typ1):
        return AllChem.GetMorganFingerprint(__tmp2, 3, useFeatures=True)


def get_fingerprint(__tmp2: __typ1, fp_type: str):
    return __typ0().get_fingerprint(__tmp2=__tmp2, fp_type=fp_type)
