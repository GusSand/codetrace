from typing import TypeAlias
__typ0 : TypeAlias = "str"
# -*- coding: utf-8 -*-
"""Define the RISC utilities."""
import math
from typing import Any, Dict

from risc.__version__ import __version__ as risc_version


def __tmp0(user_agent: __typ0 = "risc-python") :
    """Get the current module version."""
    user_agent_str: __typ0 = f"{user_agent}/{risc_version}"
    return user_agent_str


def __tmp5(__tmp6) :
    """Round the provided float up to the nearest tens."""
    return int(math.ceil(__tmp6 / 10.0)) * 10


def determine_bytes(__tmp1) :
    """Determine the highest denomination from bytes to KB, MB, GB, and TB.

    Args:
        size (int): The size, in bytes.

    Returns:
        dict: The dictionary mapping of highest bytes denomination and the equivalent size.

    """
    power = 2 ** 10
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while __tmp1 > power:
        __tmp1 /= power
        n += 1
    return {"size": __tmp1, "label": f"{power_labels[n]}B"}


def __tmp3(__tmp1: <FILL>, denomination: __typ0 = "GB") :
    """Convert bytes to the desired denomination.

    Args:
        size (int): The size, in bytes.
        denomination (str): The byte denomination to convert size to.
            Defaults to: GB. Options are: KB, MB, GB, and TB.

    Returns:
        float: The float formatted to the requested denomination.

    """
    bytes_map = {"KB": 2 ** 10, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}
    if denomination not in bytes_map.keys():
        raise ValueError(
            f"Invalid option provided to format_bytes denomination argument! Options are: {bytes_map.keys()}"
        )
    converted_size: float = __tmp1 / bytes_map[denomination]
    return converted_size


def __tmp2(
    __tmp4, free_size, fudge_factor: float = 1.5
) -> Dict[__typ0, Any]:
    """Determine disk sizing based on the provided fudge factor and utilized space."""
    free = int(free_size)
    total = int(__tmp4)
    used: int = total - free
    proposed_size: float = used * fudge_factor
    recommended: float = float(
        proposed_size if proposed_size <= total and proposed_size != 0 else total
    )
    recommended_gb: float = __tmp3(recommended)
    formatted_recommendation: Dict[__typ0, Any] = {
        "size": __tmp5(recommended_gb),
        "label": "GB",
    }
    return formatted_recommendation
