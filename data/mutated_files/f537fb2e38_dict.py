from typing import TypeAlias
__typ3 : TypeAlias = "Simulation_Group"
__typ1 : TypeAlias = "str"
import logging
import typing

from bloodytools.utils.simulation_objects import Simulation_Data, Simulation_Group
from bloodytools.simulations.simulator import Simulator

logger = logging.getLogger(__name__)


class __typ2(Exception):
    pass


class __typ0(Simulator):
    @classmethod
    def name(cls) :
        return "Talent Removal"

    def pre_processing(self, __tmp0: <FILL>) :
        __tmp0 = super().pre_processing(__tmp0)

        __tmp0 = self.get_additional_talent_paths(__tmp0)

        return __tmp0

    def add_simulation_data(
        self, simulation_group, __tmp0
    ) -> None:
        logger.debug("talent_simulations start")

        for i, k_v in enumerate(__tmp0["data_profile_overrides"].items()):
            human_name, simc_args = k_v

            if i == 0:
                profile = __tmp0["profile"]
            else:
                profile = {}

            simulation = Simulation_Data(
                name=self.get_profile_name(human_name, "baseline"),
                fight_style=self.fight_style,
                profile=profile,
                simc_arguments=simc_args,
                target_error=self.settings.target_error.get(self.fight_style, "0.1"),
                ptr=self.settings.ptr,
                default_actions=self.settings.default_actions,
                executable=self.settings.executable,
                iterations=self.settings.iterations,
            )

            # get talent string
            data_copy = simulation.copy()
            data_copy.iterations = "1"
            data_copy.simc_arguments = (
                data_copy.get_simc_arguments_from_profile(__tmp0["profile"])
                + data_copy.simc_arguments
            )
            tmp_group = __typ3(data_copy, name="extract_talents")
            tmp_group.simulate()
            if tmp_group.profiles[0].json_data:
                talent_string = "talents=" + self._get_talents(
                    tmp_group.profiles[0].json_data
                )
                if talent_string not in __tmp0["data_profile_overrides"][human_name]:
                    __tmp0["data_profile_overrides"][human_name].append(
                        talent_string
                    )

            if i == 0:
                if self.settings.custom_apl:
                    with open("custom_apl.txt") as f:
                        custom_apl = f.read()
                    simulation.simc_arguments.append("# custom_apl")
                    simulation.simc_arguments.append(custom_apl)

                if self.settings.custom_fight_style:
                    with open("custom_fight_style.txt") as f:
                        custom_fight_style = f.read()
                    simulation.simc_arguments.append("# custom_fight_style")
                    simulation.simc_arguments.append(custom_fight_style)

            simulation_group.add(simulation)

            # create simulations for each missing talent
            talent_strings: typing.List[__typ1] = [
                args
                for args in simc_args
                if args.startswith("talents=")
                or args.startswith("class_talents=")
                or args.startswith("spec_talents=")
            ]
            other_args = [arg for arg in simc_args if arg not in talent_strings]
            for talent_string in talent_strings:
                if talent_string.startswith("talents="):
                    continue
                other_talent_strings = [s for s in talent_strings if s != talent_string]
                prefix = talent_string.split("=")[0]
                cleaned_talents = talent_string.split("=")[1].split("#")[0].strip()
                talents = cleaned_talents.split("/")
                for talent in talents:
                    talent_id, invested_points = talent.split(":")
                    if int(invested_points) < 1:
                        continue

                    other_talents = [
                        t for t in talents if t != talent and int(t.split(":")[-1]) > 0
                    ]

                    active_talents = "=".join(
                        [
                            prefix,
                            "/".join(
                                other_talents
                                + [talent_id + ":" + __typ1(int(invested_points) - 1)]
                            ),
                        ]
                    )
                    logger.debug(f"{active_talents=}")

                    # TODO: continue here. rebuild the current talent string, add other simc_args too
                    simulation = Simulation_Data(
                        name=self.get_profile_name(human_name, talent_id),
                        fight_style=self.fight_style,
                        profile=profile,
                        simc_arguments=other_talent_strings
                        + other_args
                        + [active_talents],
                        target_error=self.settings.target_error.get(
                            self.fight_style, "0.1"
                        ),
                        ptr=self.settings.ptr,
                        default_actions=self.settings.default_actions,
                        executable=self.settings.executable,
                        iterations=self.settings.iterations,
                    )
                    simulation_group.add(simulation)

    def post_processing(self, __tmp0: dict) -> dict:
        __tmp0 = super().post_processing(__tmp0)

        __tmp0 = self.create_sorted_key_key_value_data(__tmp0)

        logger.debug("talent_simulations end")
        return __tmp0
