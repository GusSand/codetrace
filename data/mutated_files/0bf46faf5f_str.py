from typing import TypeAlias
__typ1 : TypeAlias = "int"
__typ0 : TypeAlias = "float"
# -*- coding: utf-8 -*-
"""Define the RISC utilities."""
import math
from typing import Any, Dict

from risc.__version__ import __version__ as risc_version


def __tmp0(user_agent: str = "risc-python") :
    """Get the current module version."""
    user_agent_str: str = f"{user_agent}/{risc_version}"
    return user_agent_str


def __tmp6(x) :
    """Round the provided float up to the nearest tens."""
    return __typ1(math.ceil(x / 10.0)) * 10


def __tmp4(__tmp1) :
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


def __tmp3(__tmp1: __typ0, denomination: str = "GB") :
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
    converted_size: __typ0 = __tmp1 / bytes_map[denomination]
    return converted_size


def __tmp2(
    __tmp5: <FILL>, free_size, fudge_factor: __typ0 = 1.5
) :
    """Determine disk sizing based on the provided fudge factor and utilized space."""
    free = __typ1(free_size)
    total = __typ1(__tmp5)
    used: __typ1 = total - free
    proposed_size: __typ0 = used * fudge_factor
    recommended: __typ0 = __typ0(
        proposed_size if proposed_size <= total and proposed_size != 0 else total
    )
    recommended_gb: __typ0 = __tmp3(recommended)
    formatted_recommendation: Dict[str, Any] = {
        "size": __tmp6(recommended_gb),
        "label": "GB",
    }
    return formatted_recommendation
