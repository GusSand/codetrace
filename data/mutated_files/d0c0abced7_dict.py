from typing import TypeAlias
__typ0 : TypeAlias = "str"
import logging

from bloodytools.simulations.simulator import Simulator
from bloodytools.utils.simulation_objects import Simulation_Data, Simulation_Group

logger = logging.getLogger(__name__)


class RaceSimulator(Simulator):
    @classmethod
    def name(__tmp2) :
        return "Races"

    def __tmp0(
        __tmp1,
        simulation_group,
        __tmp3: <FILL>,
    ) :
        profile = __tmp3["profile"]

        for race in __tmp1.wow_spec.wow_class.races:
            simulation_data = Simulation_Data(
                name=race.full_name,
                fight_style=__tmp1.fight_style,
                profile=profile,
                simc_arguments=["race={}".format(race.simc_name)],
                target_error=__tmp1.settings.target_error.get(__tmp1.fight_style, "0.1"),
                ptr=__tmp1.settings.ptr,
                default_actions=__tmp1.settings.default_actions,
                executable=__tmp1.settings.executable,
                iterations=__tmp1.settings.iterations,
                remove_files=not __tmp1.settings.keep_files,
            )

            if race == __tmp1.wow_spec.wow_class.races[0]:
                custom_apl = None
                if __tmp1.settings.custom_apl:
                    with open("custom_apl.txt") as f:
                        custom_apl = f.read()
                if custom_apl:
                    simulation_data.simc_arguments.append("# custom_apl")
                    simulation_data.simc_arguments.append(custom_apl)

                custom_fight_style = None
                if __tmp1.settings.custom_fight_style:
                    with open("custom_fight_style.txt") as f:
                        custom_fight_style = f.read()
                if custom_fight_style:
                    simulation_data.simc_arguments.append("# custom_fight_style")
                    simulation_data.simc_arguments.append(custom_fight_style)

            if race.simc_name == "zandalari_troll":
                simulation_data.simc_arguments.append("zandalari_loa=kimbul")
                simulation_data.name += " Kimbul"

                # add additional zandalari profiles
                for loa in ["bwonsamdi", "paku"]:
                    tmp_data = simulation_data.copy()
                    tmp_data.name = f"{race.full_name} {loa.title()}"
                    tmp_data.simc_arguments += [f"zandalari_loa={loa}"]

                    simulation_group.add(tmp_data)

            simulation_group.add(simulation_data)

    def post_processing(__tmp1, __tmp3) -> dict:
        __tmp3 = super().post_processing(__tmp3)

        # add translations
        for race in __tmp1.wow_spec.wow_class.races:
            __tmp3["translations"][race.full_name] = race.translations.get_dict()

            if "Zandalari" in race.full_name:
                loas = filter(
                    lambda name: race.full_name in name, __tmp3["data"].keys()
                )

                for full_name in loas:
                    loa = full_name.split(" ")[-1]
                    __tmp3["translations"][full_name] = race.translations.get_dict()
                    for lang in __tmp3["translations"][full_name]:
                        __tmp3["translations"][full_name][lang] = " ".join(
                            [
                                __tmp3["translations"][full_name][lang],
                                loa,
                            ]
                        )

        __tmp3 = __tmp1.create_sorted_key_value_data(__tmp3)

        return __tmp3
