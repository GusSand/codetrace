from typing import TypeAlias
__typ0 : TypeAlias = "str"
import json
import os
import re
import subprocess
import time
import zipfile

import config.config

all_cap_csv = re.compile(r'capture-[0-9]+\.(cap|csv)$')


def __tmp4(__tmp0: <FILL>, path: __typ0) :
    with open(path, 'w') as save_file:
        save_file.writelines(json.dumps(__tmp0, sort_keys=True, indent=4))


def __tmp3(path) -> dict:
    with open(path, 'r') as save_file:
        return json.load(save_file)


def __tmp2(__tmp1: config.config.Settings):
    os.makedirs(__tmp1.zip_path, exist_ok=True)

    # find out the current container number
    # we dont't want to override anything in case of a restart
    zip_ctr = 0
    while True:
        filename = f'container-{zip_ctr}.zip'
        if not os.path.isfile(os.path.join(__tmp1.zip_path, filename)):
            break
        zip_ctr += 1

    print(f"\tFirst Container: container-{zip_ctr}.zip")

    saved_files = set()

    while True:
        files = os.listdir(__tmp1.capture_path)

        zip_list = list()
        candidates = list()

        # first we find all .cap and .csv file
        for f in files:
            if f not in saved_files:
                match = all_cap_csv.match(f)

                if match is not None:
                    candidates.append(match.group(0))

        candidates = sorted(candidates)
        zip_list = candidates[:-__tmp1.zip_file_buffer]

        print(zip_list)

        # make sure we have enough files (at least MinGroupSize)
        if len(zip_list) >= int(__tmp1.zip_group_size):
            filename = f'container-{zip_ctr}.zip'
            with zipfile.ZipFile(os.path.join(__tmp1.zip_path, filename), 'w') as zipper:
                for f in zip_list:
                    zipper.write(os.path.join(__tmp1.capture_path, f),
                                 f, compress_type=zipfile.ZIP_DEFLATED)
                    saved_files.add(f)
                    # because we have likely no permission to clear the file
                    # we need to sudo our way around it
                    subprocess.call("cat /dev/null | sudo tee {}".format(os.path.join(__tmp1.capture_path, f)),
                                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            zip_ctr += 1

        time.sleep(__tmp1.zip_freq)
