from typing import TypeAlias
__typ0 : TypeAlias = "str"
# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

"""
Extract specific parameters.
"""

import argparse
import os
from typing import Dict, List

import mxnet as mx
import numpy as np

from . import arguments
from . import constants as C
from . import utils
from .log import setup_main_logger, log_sockeye_version

logger = setup_main_logger(__name__, console=True, file_logging=False)


def __tmp0(__tmp7,
             __tmp6,
             __tmp5) :
    """
    Extract specific parameters from a given base.

    :param param_names: Names of parameters to be extracted.
    :param params: Mapping from parameter names to the actual NDArrays parameters.
    :param ext_params: Extracted parameter dictionary.
    :return: Remaining names of parameters to be extracted.
    """
    remaining_param_names = list(__tmp7)
    for name in __tmp7:
        if name in __tmp6:
            logger.info("\tFound '%s': shape=%s", name, __typ0(__tmp6[name].shape))
            __tmp5[name] = __tmp6[name].asnumpy()
            remaining_param_names.remove(name)
    return remaining_param_names


def __tmp3(__tmp2,
            __tmp7,
            list_all: <FILL>) :
    """
    Extract specific parameters given their names.

    :param param_path: Path to the parameter file.
    :param param_names: Names of parameters to be extracted.
    :param list_all: List names of all available parameters.
    :return: Extracted parameter dictionary.
    """
    logger.info("Loading parameters from '%s'", __tmp2)
    arg_params, aux_params = utils.load_params(__tmp2)

    __tmp5 = {}  # type: Dict[str, np.ndarray]
    __tmp7 = __tmp0(__tmp7, arg_params, __tmp5)
    __tmp7 = __tmp0(__tmp7, aux_params, __tmp5)

    if len(__tmp7) > 0:
        logger.info("The following parameters were not found:")
        for name in __tmp7:
            logger.info("\t%s", name)
        logger.info("Check the following availabilities")
        list_all = True

    if list_all:
        if arg_params:
            logger.info("Available arg parameters:")
            for name in arg_params:
                logger.info("\t%s: shape=%s", name, __typ0(arg_params[name].shape))
        if aux_params:
            logger.info("Available aux parameters:")
            for name in aux_params:
                logger.info("\t%s: shape=%s", name, __typ0(aux_params[name].shape))

    return __tmp5


def main():
    """
    Commandline interface to extract parameters.
    """
    __tmp6 = argparse.ArgumentParser(description="Extract specific parameters.")
    arguments.add_extract_args(__tmp6)
    __tmp1 = __tmp6.parse_args()
    __tmp4(__tmp1)


def __tmp4(__tmp1):
    log_sockeye_version(logger)

    if os.path.isdir(__tmp1.input):
        __tmp2 = os.path.join(__tmp1.input, C.PARAMS_BEST_NAME)
    else:
        __tmp2 = __tmp1.input
    __tmp5 = __tmp3(__tmp2, __tmp1.names, __tmp1.list_all)

    if len(__tmp5) > 0:
        utils.check_condition(__tmp1.output is not None, "An output filename must be specified. (Use --output)")
        logger.info("Writing extracted parameters to '%s'", __tmp1.output)
        np.savez_compressed(__tmp1.output, **__tmp5)


if __name__ == "__main__":
    main()
