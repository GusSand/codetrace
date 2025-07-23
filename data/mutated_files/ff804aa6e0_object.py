import dataclasses
import logging
import sys
import typing

from bloodytools.utils.data_type import DataType
from simc_support.game_data.WowSpec import WowSpec, get_wow_spec

from bloodytools.utils.simc import get_simc_hash

logger = logging.getLogger(__name__)

# ! Hier sitz ich nun ich armer Tor. Bin so klug als wie zuvor.
# ! Schrieb Module und Klassen gar. Doch wozu ich sie gebar?
# ! Drum denk ich nun, ich lass sie weg. Zuvor funktionierte's also was soll der Kek(s)?


@dataclasses.dataclass
class __typ0:
    """Configuration that doesn't simulate anything but has otherwise sensible default values."""

    custom_apl: bool = False
    custom_fight_style: bool = False
    custom_profile: bool = False
    data_type: DataType = DataType.DPS
    debug: bool = False
    default_actions: str = "1"
    executable: str = "../SimulationCraft/simc"
    """Path to the executable, including the executable"""
    iterations: str = "60000"
    keep_files: bool = False
    # affects trinkets
    max_ilevel: int = 457
    # affects trinkets
    min_ilevel: int = 411
    pretty: bool = False
    profileset_work_threads: str = "2"
    ptr: str = "0"
    raidbots: bool = False
    remove_files: bool = False
    secondary_distributions_step_size: int = 10
    simc_hash: str = ""
    single_sim: str = ""
    # Affects secondary distribution simulations
    # if no list is provided for a class-spec, all dps talent combinations will be run. If you want to only sim the base profiles, set 'talent_permutations' to False
    # talent_list = {
    #   WowSpec.ELEMENTAL: [
    #     "2301022",
    #   ],
    # }  # example for a talent list for Elemental Shamans
    # set to False, to sim only the base profile talent combinations
    talent_list: typing.Dict[WowSpec, typing.Iterable[str]] = dataclasses.field(
        default_factory=dict
    )
    talent_permutations: bool = False
    target_error: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    threads: str = ""
    tier: str = "30"
    use_raidbots: bool = False
    write_humanreadable_secondary_distribution_file: bool = False
    apikey: str = ""
    simulator_type_names: typing.List[str] = dataclasses.field(default_factory=list)
    wow_class_spec_names: typing.List[typing.Tuple[str, str]] = dataclasses.field(
        default_factory=list
    )
    fight_styles: typing.List[str] = dataclasses.field(default_factory=list)

    log_warnings: bool = True
    """Log warnings for Config creation."""

    def __tmp2(__tmp1, *__tmp0, **kwargs) -> None:
        __tmp1.target_error["patchwerk"] = "0.1"
        __tmp1.target_error["hecticaddcleave"] = "0.2"
        __tmp1.target_error["beastlord"] = "0.2"
        __tmp1.set_simc_hash()

    def set_simc_hash(__tmp1) -> None:
        new_hash = get_simc_hash(__tmp1.executable, __tmp1.log_warnings)
        if new_hash:
            __tmp1.simc_hash = new_hash

    @property
    def __tmp5(__tmp1) -> typing.List[WowSpec]:
        return [get_wow_spec(*name_tuple) for name_tuple in __tmp1.wow_class_spec_names]

    @classmethod
    def __tmp4(__tmp3, __tmp0: <FILL>) :
        config = __tmp3(log_warnings=False)

        config.log_warnings = True

        if __tmp0.single_sim:  # type: ignore
            logger.debug("-s / --single_sim detected")
            try:
                (
                    simulation_type,
                    wow_class,
                    wow_spec,
                    fight_style,
                ) = __tmp0.single_sim.split(  # type: ignore
                    ","
                )
            except ValueError:
                logger.error("-s / --single_sim arg is missing parameters. Read -h.")
                sys.exit("Input error. Bloodytools terminates.")

            config.wow_class_spec_names = [
                (wow_class, wow_spec),
            ]

            config.fight_styles = [
                fight_style,
            ]
            if fight_style not in config.target_error:
                config.target_error[fight_style] = "0.1"

            config.simulator_type_names = [
                simulation_type,
            ]

        if __tmp0.executable:  # type: ignore
            config.executable = __tmp0.executable  # type: ignore
            logger.debug("Set executable to {}".format(config.executable))

        if __tmp0.threads:  # type: ignore
            config.threads = __tmp0.threads  # type: ignore
            logger.debug("Set threads to {}".format(config.threads))

        if __tmp0.profileset_work_threads:  # type: ignore
            config.profileset_work_threads = __tmp0.profileset_work_threads  # type: ignore
            logger.debug(
                "Set profileset_work_threads to {}".format(
                    config.profileset_work_threads
                )
            )

        if __tmp0.ptr:  # type: ignore
            config.ptr = "1"
        else:
            config.ptr = "0"

        config.custom_profile = __tmp0.custom_profile  # type: ignore
        config.custom_fight_style = __tmp0.custom_fight_style  # type: ignore
        config.custom_apl = __tmp0.custom_apl  # type: ignore
        if __tmp0.custom_apl:  # type: ignore
            config.default_actions = "0"

        if __tmp0.target_error:  # type: ignore
            for fight_style in config.target_error.keys():
                config.target_error[fight_style] = __tmp0.target_error  # type: ignore

        config.use_raidbots = __tmp0.raidbots  # type: ignore
        config.keep_files = __tmp0.keep_files  # type: ignore
        config.pretty = __tmp0.pretty  # type: ignore

        config.set_simc_hash()

        return config
