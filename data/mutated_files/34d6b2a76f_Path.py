from typing import TypeAlias
__typ1 : TypeAlias = "ConfigDict"
import yaml
import argparse
import appdirs
from pathlib import Path
from config.config import Config, ConfigDict
from config.default_config import default_yaml


def __tmp2() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    args, _ = parser.parse_known_args()

    if args.config is None:
        config_dir = appdirs.user_config_dir('spytrack')
        return Path(config_dir).joinpath("config.yaml")
    else:
        return Path(args.config)


class ConfigParseException(BaseException):
    pass


class __typ0:
    def __tmp3(__tmp1, file: <FILL>) :
        __tmp1.file = file

    def __tmp4(__tmp1) :
        try:
            if not __tmp1.file.exists():
                __tmp1.file.parent.mkdir(parents=True, exist_ok=True)
                values = yaml.safe_load(default_yaml)
                __tmp1._persist(values)
            else:
                values = yaml.safe_load(__tmp1.file.read_text())
            return Config.parse(values)
        except yaml.YAMLError:
            raise ConfigParseException

    def __tmp0(__tmp1, config) :
        dump = {
            "daemon": {
                "host": config.host,
                "port": config.port,
            },
            "gui": {
                "run_daemon": config.run_daemon,
                "interval": config.interval,
                "start_day_time": config.start_day_time,
                "projects": config.projects.to_json()}
        }
        __tmp1._persist(dump)

    def _persist(__tmp1, dump) :
        with __tmp1.file.open('w') as outfile:
            yaml.dump(dump, outfile, default_flow_style=False)
