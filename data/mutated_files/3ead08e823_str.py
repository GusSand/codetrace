"""Simulate and then collect all data of a tier."""
from bloodytools.utils.config import Config
from simc_support.game_data import WowSpec
from bloodytools.main import main as main_routine
import dataclasses
import logging
import json
import enum
from rich.console import Console
from rich.table import Table
import typing
import os

logging.basicConfig(level=logging.ERROR)

logger = logging.getLogger()

TIER = "30"
EXECUTABLE = "../simc/simc.exe"
FIGHT_STYLE = "castingpatchwerk"

# MISSING_PROFILES = (
#     ("Druid", "Restoration"),
#     ("Evoker", "Preservation"),
#     ("Monk", "Mistweaver"),
#     ("Paladin", "Holy"),
#     ("Priest", "Holy"),
#     ("Priest", "Discipline"),
#     ("Shaman", "Restoration"),
#     # ???
# )


def __tmp9(__tmp4) :
    config = Config(
        executable=EXECUTABLE,
        pretty=True,
        tier=TIER,
        wow_class_spec_names=__tmp4,
        simulator_type_names=["tier_set"],
        fight_styles=[FIGHT_STYLE],
    )
    main_routine(config)


@dataclasses.dataclass
class TierData:
    wow_spec: str
    wow_class: str
    no_tier_dps: int
    tier_2pc_dps: int
    tier_4pc_dps: int


def __tmp10(__tmp11) :
    return __tmp11.replace(" ", "_").lower()


def __tmp6(__tmp4) :
    data: typing.List[TierData] = []

    print(f"Listed class-spec combination below don't  have a T{TIER} profile yet.")
    for wow_class, wow_spec in __tmp4:
        file_path = f"results/tier_set/{__tmp10(wow_class)}_{__tmp10(wow_spec)}_{FIGHT_STYLE}.json"

        if not os.path.exists(file_path):
            print(f'("{wow_class}", "{wow_spec}"),')
            continue

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:
            loaded_file = json.load(f)
        # data.custom profile
        #   2p
        #   4p
        #   no tier
        data.append(
            TierData(
                wow_class=wow_class,
                wow_spec=wow_spec,
                no_tier_dps=loaded_file["data"][f"T{TIER}"]["no tier"],
                tier_2pc_dps=loaded_file["data"][f"T{TIER}"]["2p"],
                tier_4pc_dps=loaded_file["data"][f"T{TIER}"]["4p"],
            )
        )
    return data


def __tmp8(data, __tmp0) :
    return int(getattr(data, __tmp0)) - data.no_tier_dps


def __tmp5(data, __tmp0: <FILL>) :
    return (int(getattr(data, __tmp0)) - data.no_tier_dps) / data.no_tier_dps * 100.0


def __tmp2(
    data,
    __tmp3,
    __tmp7,
) :
    sorted_data = sorted(
        data,
        key=lambda tier_data: __tmp3(tier_data, "tier_4pc_dps"),
        reverse=True,
    )

    table = Table(__tmp7=__tmp7)

    table.add_column("Spec")
    table.add_column("2p", justify="right")
    table.add_column("2p + 4p", justify="right")

    for tier_data in sorted_data:
        table.add_row(
            " ".join([tier_data.wow_spec, tier_data.wow_class]),
            f"{float(__tmp3(tier_data, 'tier_2pc_dps')):5>.2f}",
            f"{float(__tmp3(tier_data, 'tier_4pc_dps')):5>.2f}",
        )

    console = Console()
    console.print(table)


def __tmp1(
    __tmp4
) :
    simc_path = os.path.join(*EXECUTABLE.split("/")[:-1])
    return [
        spec
        for spec in __tmp4
        if os.path.exists(
            f"{simc_path}/profiles/Tier{TIER}/T{TIER}_{spec[0]}_{spec[1]}.simc"
        )
    ]


def main() -> None:
    __tmp4 = [(s.wow_class.full_name, s.full_name) for s in WowSpec.WOWSPECS]
    __tmp4 = __tmp1(__tmp4)
    # simulate_tier_data(specs)
    data = __tmp6(__tmp4)

    __tmp2(data, __tmp8, f"Absolute gain T{TIER}")

    __tmp2(data, __tmp5, f"Relative gain T{TIER} in %")


if __name__ == "__main__":
    main()
