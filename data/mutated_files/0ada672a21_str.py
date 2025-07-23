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


def _extract(__tmp2,
             params,
             ext_params: Dict[str, np.ndarray]) :
    """
    Extract specific parameters from a given base.

    :param param_names: Names of parameters to be extracted.
    :param params: Mapping from parameter names to the actual NDArrays parameters.
    :param ext_params: Extracted parameter dictionary.
    :return: Remaining names of parameters to be extracted.
    """
    remaining_param_names = list(__tmp2)
    for name in __tmp2:
        if name in params:
            logger.info("\tFound '%s': shape=%s", name, str(params[name].shape))
            ext_params[name] = params[name].asnumpy()
            remaining_param_names.remove(name)
    return remaining_param_names


def __tmp1(param_path: <FILL>,
            __tmp2,
            list_all: bool) :
    """
    Extract specific parameters given their names.

    :param param_path: Path to the parameter file.
    :param param_names: Names of parameters to be extracted.
    :param list_all: List names of all available parameters.
    :return: Extracted parameter dictionary.
    """
    logger.info("Loading parameters from '%s'", param_path)
    arg_params, aux_params = utils.load_params(param_path)

    ext_params = {}  # type: Dict[str, np.ndarray]
    __tmp2 = _extract(__tmp2, arg_params, ext_params)
    __tmp2 = _extract(__tmp2, aux_params, ext_params)

    if len(__tmp2) > 0:
        logger.info("The following parameters were not found:")
        for name in __tmp2:
            logger.info("\t%s", name)
        logger.info("Check the following availabilities")
        list_all = True

    if list_all:
        if arg_params:
            logger.info("Available arg parameters:")
            for name in arg_params:
                logger.info("\t%s: shape=%s", name, str(arg_params[name].shape))
        if aux_params:
            logger.info("Available aux parameters:")
            for name in aux_params:
                logger.info("\t%s: shape=%s", name, str(aux_params[name].shape))

    return ext_params


def main():
    """
    Commandline interface to extract parameters.
    """
    params = argparse.ArgumentParser(description="Extract specific parameters.")
    arguments.add_extract_args(params)
    __tmp0 = params.parse_args()
    extract_parameters(__tmp0)


def extract_parameters(__tmp0):
    log_sockeye_version(logger)

    if os.path.isdir(__tmp0.input):
        param_path = os.path.join(__tmp0.input, C.PARAMS_BEST_NAME)
    else:
        param_path = __tmp0.input
    ext_params = __tmp1(param_path, __tmp0.names, __tmp0.list_all)

    if len(ext_params) > 0:
        utils.check_condition(__tmp0.output is not None, "An output filename must be specified. (Use --output)")
        logger.info("Writing extracted parameters to '%s'", __tmp0.output)
        np.savez_compressed(__tmp0.output, **ext_params)


if __name__ == "__main__":
    main()
