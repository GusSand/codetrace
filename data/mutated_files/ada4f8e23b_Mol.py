from rdkit.Chem import AllChem, Mol
from rdkit.Chem.AtomPairs.Sheridan import GetBPFingerprint, GetBTFingerprint
from rdkit.Chem.Pharm2D import Generate, Gobbi_Pharm2D


class _FingerprintCalculator:
    """
    Calculate the fingerprint while avoiding a series of if-else.
    See recipe 8.21 of the book "Python Cookbook".

    To support a new type of fingerprint, just add a function "get_fpname(self, mol)".
    """

    def get_fingerprint(__tmp0, __tmp3: Mol, fp_type):
        method_name = 'get_' + fp_type
        method = getattr(__tmp0, method_name)
        if method is None:
            raise Exception(f'{fp_type} is not a supported fingerprint type.')
        return method(__tmp3)

    def get_AP(__tmp0, __tmp3: Mol):
        return AllChem.GetAtomPairFingerprint(__tmp3, maxLength=10)

    def __tmp2(__tmp0, __tmp3):
        return Generate.Gen2DFingerprint(__tmp3, Gobbi_Pharm2D.factory)

    def get_BPF(__tmp0, __tmp3):
        return GetBPFingerprint(__tmp3)

    def get_BTF(__tmp0, __tmp3: Mol):
        return GetBTFingerprint(__tmp3)

    def get_PATH(__tmp0, __tmp3):
        return AllChem.RDKFingerprint(__tmp3)

    def get_ECFP4(__tmp0, __tmp3: Mol):
        return AllChem.GetMorganFingerprint(__tmp3, 2)

    def get_ECFP6(__tmp0, __tmp3: Mol):
        return AllChem.GetMorganFingerprint(__tmp3, 3)

    def get_FCFP4(__tmp0, __tmp3: Mol):
        return AllChem.GetMorganFingerprint(__tmp3, 2, useFeatures=True)

    def __tmp1(__tmp0, __tmp3: <FILL>):
        return AllChem.GetMorganFingerprint(__tmp3, 3, useFeatures=True)


def get_fingerprint(__tmp3: Mol, fp_type: str):
    return _FingerprintCalculator().get_fingerprint(__tmp3=__tmp3, fp_type=fp_type)
