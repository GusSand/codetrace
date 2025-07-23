from rdkit.Chem import AllChem, Mol
from rdkit.Chem.AtomPairs.Sheridan import GetBPFingerprint, GetBTFingerprint
from rdkit.Chem.Pharm2D import Generate, Gobbi_Pharm2D


class __typ0:
    """
    Calculate the fingerprint while avoiding a series of if-else.
    See recipe 8.21 of the book "Python Cookbook".

    To support a new type of fingerprint, just add a function "get_fpname(self, mol)".
    """

    def get_fingerprint(__tmp1, mol, fp_type):
        method_name = 'get_' + fp_type
        method = getattr(__tmp1, method_name)
        if method is None:
            raise Exception(f'{fp_type} is not a supported fingerprint type.')
        return method(mol)

    def get_AP(__tmp1, mol):
        return AllChem.GetAtomPairFingerprint(mol, maxLength=10)

    def get_PHCO(__tmp1, mol: Mol):
        return Generate.Gen2DFingerprint(mol, Gobbi_Pharm2D.factory)

    def __tmp0(__tmp1, mol):
        return GetBPFingerprint(mol)

    def get_BTF(__tmp1, mol):
        return GetBTFingerprint(mol)

    def get_PATH(__tmp1, mol):
        return AllChem.RDKFingerprint(mol)

    def get_ECFP4(__tmp1, mol: <FILL>):
        return AllChem.GetMorganFingerprint(mol, 2)

    def get_ECFP6(__tmp1, mol):
        return AllChem.GetMorganFingerprint(mol, 3)

    def get_FCFP4(__tmp1, mol):
        return AllChem.GetMorganFingerprint(mol, 2, useFeatures=True)

    def get_FCFP6(__tmp1, mol):
        return AllChem.GetMorganFingerprint(mol, 3, useFeatures=True)


def get_fingerprint(mol: Mol, fp_type):
    return __typ0().get_fingerprint(mol=mol, fp_type=fp_type)
