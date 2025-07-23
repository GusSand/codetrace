from typing import List

from guacamol.distribution_matching_generator import DistributionMatchingGenerator


class __typ0(DistributionMatchingGenerator):
    """
    Mock generator that returns pre-defined molecules,
    possibly split in several calls
    """

    def __tmp1(__tmp0, molecules: List[str]) :
        __tmp0.molecules = molecules
        __tmp0.cursor = 0

    def generate(__tmp0, number_samples: <FILL>) -> List[str]:
        end = __tmp0.cursor + number_samples

        sampled_molecules = __tmp0.molecules[__tmp0.cursor:end]
        __tmp0.cursor = end
        return sampled_molecules
