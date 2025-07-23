from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ2 : TypeAlias = "Simulation_Group"
from bloodytools.utils.simulation_objects import Simulation_Data, Simulation_Group
from .simulator import Simulator


class MissingTalentTreePathFileError(Exception):
    pass


class __typ1(Simulator):
    @classmethod
    def __tmp3(cls) :
        return "Tier Set"

    def profile_split_character(__tmp0) -> __typ0:
        return "|||"

    def pre_processing(__tmp0, __tmp2) -> dict:
        __tmp2 = super().pre_processing(__tmp2)

        __tmp2 = __tmp0.get_additional_talent_paths(__tmp2)

        return __tmp2

    def __tmp1(
        __tmp0, simulation_group, __tmp2: <FILL>
    ) -> None:
        tier_mapping = {
            "no tier": [
                "set_bonus=tier29_2pc=0",
                "set_bonus=tier29_4pc=0",
                "set_bonus=tier30_2pc=0",
                "set_bonus=tier30_4pc=0",
            ],
            "2p": [
                "set_bonus=tier30_2pc=1",
                "set_bonus=tier30_4pc=0",
            ],
            "4p": [
                "set_bonus=tier30_2pc=1",
                "set_bonus=tier30_4pc=1",
            ],
        }

        for tier, simc_input in tier_mapping.items():
            for i, k_v in enumerate(__tmp2["data_profile_overrides"].items()):
                human_name, simc_args = k_v

                if len(simulation_group.profiles) == 0:
                    profile = __tmp2["profile"]
                else:
                    profile = {}

                clear_talents = [
                    "talents=",
                    "spec_talents=",
                    "class_talents=",
                ]

                merged_simc_args = simc_input + clear_talents + simc_args

                data = Simulation_Data(
                    __tmp3=__tmp0.profile_split_character().join([human_name, tier]),
                    simc_arguments=merged_simc_args,
                    fight_style=__tmp0.fight_style,
                    profile=profile,
                    target_error=__tmp0.settings.target_error.get(
                        __tmp0.fight_style, "0.1"
                    ),
                    ptr=__tmp0.settings.ptr,
                    default_actions=__tmp0.settings.default_actions,
                    executable=__tmp0.settings.executable,
                    iterations=__tmp0.settings.iterations,
                )

                # get talent string
                data_copy = data.copy()
                data_copy.iterations = "1"
                data_copy.simc_arguments = (
                    data_copy.get_simc_arguments_from_profile(__tmp2["profile"])
                    + data_copy.simc_arguments
                )
                tmp_group = __typ2(data_copy, __tmp3="extract_talents")
                tmp_group.simulate()
                if tmp_group.profiles[0].json_data:
                    talents = "talents=" + __tmp0._get_talents(
                        tmp_group.profiles[0].json_data
                    )
                    if talents not in __tmp2["data_profile_overrides"][human_name]:
                        __tmp2["data_profile_overrides"][human_name].append(talents)

                if len(simulation_group.profiles) == 0:
                    custom_apl = None
                    if __tmp0.settings.custom_apl:
                        with open("custom_apl.txt") as f:
                            custom_apl = f.read()
                    if custom_apl:
                        data.simc_arguments.append("# custom_apl")
                        data.simc_arguments.append(custom_apl)

                    custom_fight_style = None
                    if __tmp0.settings.custom_fight_style:
                        with open("custom_fight_style.txt") as f:
                            custom_fight_style = f.read()
                    if custom_fight_style:
                        data.simc_arguments.append("# custom_fight_style")
                        data.simc_arguments.append(custom_fight_style)

                simulation_group.add(data)

    def post_processing(__tmp0, __tmp2) -> dict:
        __tmp2 = super().post_processing(__tmp2)

        __tmp0.create_sorted_key_key_value_data(__tmp2)

        return __tmp2
