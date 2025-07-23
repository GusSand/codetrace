from typing import TypeAlias
__typ0 : TypeAlias = "Path"
__typ2 : TypeAlias = "ConfigDict"
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
        return __typ0(config_dir).joinpath("config.yaml")
    else:
        return __typ0(args.config)


class ConfigParseException(BaseException):
    pass


class __typ1:
    def __tmp1(__tmp0, file) :
        __tmp0.file = file

    def load(__tmp0) :
        try:
            if not __tmp0.file.exists():
                __tmp0.file.parent.mkdir(parents=True, exist_ok=True)
                values = yaml.safe_load(default_yaml)
                __tmp0._persist(values)
            else:
                values = yaml.safe_load(__tmp0.file.read_text())
            return Config.parse(values)
        except yaml.YAMLError:
            raise ConfigParseException

    def save(__tmp0, config: <FILL>) :
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
        __tmp0._persist(dump)

    def _persist(__tmp0, dump) :
        with __tmp0.file.open('w') as outfile:
            yaml.dump(dump, outfile, default_flow_style=False)
