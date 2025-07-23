from typing import TypeAlias
__typ0 : TypeAlias = "float"
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


def __tmp4(__tmp2) -> None:
    config = Config(
        executable=EXECUTABLE,
        pretty=True,
        tier=TIER,
        wow_class_spec_names=__tmp2,
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


def simc_name(name: str) :
    return name.replace(" ", "_").lower()


def load_tier_data(__tmp2: typing.List[typing.Tuple[str, str]]) -> typing.List[TierData]:
    data: typing.List[TierData] = []

    print(f"Listed class-spec combination below don't  have a T{TIER} profile yet.")
    for wow_class, wow_spec in __tmp2:
        file_path = f"results/tier_set/{simc_name(wow_class)}_{simc_name(wow_spec)}_{FIGHT_STYLE}.json"

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


def absolute_gain(data, target) -> __typ0:
    return int(getattr(data, target)) - data.no_tier_dps


def __tmp3(data: TierData, target: str) :
    return (int(getattr(data, target)) - data.no_tier_dps) / data.no_tier_dps * 100.0


def __tmp0(
    data,
    __tmp1,
    title: <FILL>,
) -> None:
    sorted_data = sorted(
        data,
        key=lambda tier_data: __tmp1(tier_data, "tier_4pc_dps"),
        reverse=True,
    )

    table = Table(title=title)

    table.add_column("Spec")
    table.add_column("2p", justify="right")
    table.add_column("2p + 4p", justify="right")

    for tier_data in sorted_data:
        table.add_row(
            " ".join([tier_data.wow_spec, tier_data.wow_class]),
            f"{__typ0(__tmp1(tier_data, 'tier_2pc_dps')):5>.2f}",
            f"{__typ0(__tmp1(tier_data, 'tier_4pc_dps')):5>.2f}",
        )

    console = Console()
    console.print(table)


def filter_by_existing_profiles(
    __tmp2
) -> typing.List[typing.Tuple[str, str]]:
    simc_path = os.path.join(*EXECUTABLE.split("/")[:-1])
    return [
        spec
        for spec in __tmp2
        if os.path.exists(
            f"{simc_path}/profiles/Tier{TIER}/T{TIER}_{spec[0]}_{spec[1]}.simc"
        )
    ]


def main() -> None:
    __tmp2 = [(s.wow_class.full_name, s.full_name) for s in WowSpec.WOWSPECS]
    __tmp2 = filter_by_existing_profiles(__tmp2)
    # simulate_tier_data(specs)
    data = load_tier_data(__tmp2)

    __tmp0(data, absolute_gain, f"Absolute gain T{TIER}")

    __tmp0(data, __tmp3, f"Relative gain T{TIER} in %")


if __name__ == "__main__":
    main()
