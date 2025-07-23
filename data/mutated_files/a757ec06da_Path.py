from pathlib import Path

import appdirs


DEREX_DIR = Path(appdirs.user_data_dir(appname="derex"))


def __tmp0(directory: <FILL>):
    if not directory.exists():
        directory.mkdir(parents=True)
