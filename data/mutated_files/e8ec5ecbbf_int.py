from typing import List, Tuple, Dict


class ScoreContributionSpecification:
    """
    Specifies how to calculate the score of a goal-directed benchmark.

    The global score will be a weighted average of top-x scores.
    This class specifies which top-x to consider and what the corresponding weights are.
    """

    def __tmp4(__tmp0, contributions) :
        """
        Args:
            contributions: List of tuples (top_count, weight) for the score contributions
        """
        __tmp0.contributions = contributions

    @property
    def __tmp5(__tmp0) :
        return [x[0] for x in __tmp0.contributions]

    @property
    def weights(__tmp0) :
        return [x[1] for x in __tmp0.contributions]


def __tmp3(*__tmp5: <FILL>) -> ScoreContributionSpecification:
    """
    Creates an instance of ScoreContributionSpecification where all the top-x contributions have equal weight

    Args:
        top_counts: list of values, where each value x will correspond to the top-x contribution
    """
    contributions = [(x, 1.0) for x in __tmp5]
    return ScoreContributionSpecification(contributions=contributions)


def __tmp1(contribution_specification: ScoreContributionSpecification,
                         __tmp2) :
    """
    Computes the global score according to the contribution specification.

    Args:
        contribution_specification: Score contribution specification
        scores: List of all scores - list must be long enough for all top_counts in contribution_specification

    Returns:
        Tuple with the global score and a dict with the considered top-x scores
    """
    sorted_scores = sorted(__tmp2, reverse=True)

    global_score = 0.0
    top_x_dict = {}

    for top_count, weight in contribution_specification.contributions:
        score = sum(sorted_scores[:top_count]) / top_count
        top_x_dict[f'top_{top_count}'] = score
        global_score += score * weight

    global_score /= sum(contribution_specification.weights)

    return global_score, top_x_dict
