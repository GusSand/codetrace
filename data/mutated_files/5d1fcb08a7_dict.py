import logging

from bloodytools.utils.simulation_objects import Simulation_Data, Simulation_Group
from bloodytools.simulations.simulator import Simulator

logger = logging.getLogger(__name__)


class __typ0(Exception):
    pass


class TalentSimulator(Simulator):
    @classmethod
    def name(__tmp3) -> str:
        return "Talents"

    def pre_processing(__tmp0, __tmp2: dict) -> dict:
        __tmp2 = super().pre_processing(__tmp2)

        __tmp2 = __tmp0.get_additional_talent_paths(__tmp2)

        return __tmp2

    def __tmp1(
        __tmp0, __tmp4, __tmp2: <FILL>
    ) -> None:
        logger.debug("talent_simulations start")

        for i, k_v in enumerate(__tmp2["data_profile_overrides"].items()):
            human_name, simc_args = k_v

            if i == 0:
                profile = __tmp2["profile"]
            else:
                profile = {}

            profile = Simulation_Data(
                name=human_name,
                fight_style=__tmp0.fight_style,
                profile=profile,
                simc_arguments=simc_args,
                target_error=__tmp0.settings.target_error.get(__tmp0.fight_style, "0.1"),
                ptr=__tmp0.settings.ptr,
                default_actions=__tmp0.settings.default_actions,
                executable=__tmp0.settings.executable,
                iterations=__tmp0.settings.iterations,
            )

            if i == 0:
                if __tmp0.settings.custom_apl:
                    with open("custom_apl.txt") as f:
                        custom_apl = f.read()
                    profile.simc_arguments.append("# custom_apl")
                    profile.simc_arguments.append(custom_apl)

                if __tmp0.settings.custom_fight_style:
                    with open("custom_fight_style.txt") as f:
                        custom_fight_style = f.read()
                    profile.simc_arguments.append("# custom_fight_style")
                    profile.simc_arguments.append(custom_fight_style)

            __tmp4.add(profile)

    def post_processing(__tmp0, __tmp2) -> dict:
        __tmp2 = super().post_processing(__tmp2)

        __tmp2 = __tmp0.create_sorted_key_value_data(__tmp2)

        logger.debug("talent_simulations end")
        return __tmp2
