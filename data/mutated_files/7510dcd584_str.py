import datetime
import logging
import subprocess

from bloodytools.utils.config import Config
from bloodytools.utils.profile_extraction import get_profile
from simc_support.game_data.WowSpec import WowSpec

__tmp7 = logging.getLogger(__name__)


def __tmp0() -> str:
    """Returns a pretty time stamp "YYYY-MM-DD HH:MM"

    Returns:
      str -- timestamp
    """
    # str(datetime.datetime.utcnow())[:-10] should be the same
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")


def __tmp2(
    __tmp1, __tmp5: WowSpec, __tmp4, __tmp3: Config
):
    """Creates as basic json dictionary. You'll need to add your data into 'data'. Can be extended.

    Arguments:
      data_type {str} -- e.g. Races, Trinkets, Azerite Traits (str is used in the title)
      wow_spec {WowSpec} -- [description]
      fight_style {str} -- [description]
      settings {Config} -- [description]

    Returns:
      dict -- [description]
    """

    __tmp7.debug("create_base_json_dict start")

    timestamp = __tmp0()

    profile = get_profile(__tmp5=__tmp5, __tmp4=__tmp4, __tmp3=__tmp3)

    # add class/ id number
    class_id = __tmp5.wow_class.id
    spec_id = __tmp5.id

    subtitle = "UTC {timestamp}".format(timestamp=timestamp)
    if __tmp3.simc_hash:
        subtitle += ' | SimC build: <a href="https://github.com/simulationcraft/simc/commit/{simc_hash}" target="blank">{simc_hash_short}</a>'.format(
            simc_hash=__tmp3.simc_hash, simc_hash_short=__tmp3.simc_hash[0:7]
        )

    try:
        bloodytools_hash = (
            subprocess.check_output(["git", "log", "-1", "--format=oneline"])
            .strip()
            .decode()
            .split(" ")[0]
        )
    except Exception:
        bloodytools_hash = None

    return {
        "data_type": "{}".format(__tmp1.lower().replace(" ", "_")),
        "timestamp": timestamp,
        "title": "{data_type} | {wow_spec} {wow_class} | {fight_style}".format(
            __tmp1=__tmp1.title(),
            wow_class=__tmp5.wow_class.full_name,
            __tmp5=__tmp5.full_name,
            __tmp4=__tmp4.title(),
        ),
        "subtitle": subtitle,
        "simc_settings": {
            "tier": __tmp3.tier,
            "fight_style": __tmp4,
            "iterations": __tmp3.iterations,
            "target_error": __tmp3.target_error.get(__tmp4, "0.1"),
            "ptr": __tmp3.ptr,
            "simc_hash": __tmp3.simc_hash,
        },
        "metadata": {
            "bloodytools": bloodytools_hash,
            "SimulationCraft": __tmp3.simc_hash,
            "timestamp": str(datetime.datetime.utcnow()),
        },
        "data": {},
        "translations": {},
        "profile": profile,
        "class_id": class_id,
        "spec_id": spec_id,
    }


def tokenize_str(__tmp6: <FILL>) -> str:
    """Return SimulationCraft appropriate name.

    Arguments:
      string {str} -- E.g. "Tawnos, Urza's Apprentice"

    Returns:
      str -- "tawnos_urzas_apprentice"
    """

    __tmp6 = __tmp6.lower().split(" (")[0]
    # cleanse name
    if (
        "__" in __tmp6
        or " " in __tmp6
        or "-" in __tmp6
        or "'" in __tmp6
        or "," in __tmp6
    ):
        return tokenize_str(
            __tmp6.replace("'", "")
            .replace("-", "")
            .replace(" ", "_")
            .replace("__", "_")
            .replace(",", "")
        )

    return __tmp6


def __tmp8(__tmp7: logging.Logger, debug=False):
    # logging to file and console
    __tmp7.setLevel(logging.DEBUG)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    if debug:
        console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    __tmp7.addHandler(console_handler)

    # file handler
    file_handler = logging.FileHandler("debug.log", "w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(filename)s / %(funcName)s:%(lineno)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    __tmp7.addHandler(file_handler)

    # error file handler
    error_handler = logging.FileHandler("error.log", "w", encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        "%(asctime)s - %(filename)s / %(funcName)s:%(lineno)s - %(levelname)s - %(message)s"
    )
    error_handler.setFormatter(error_formatter)
    __tmp7.addHandler(error_handler)

    return __tmp7
