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
Average parameters from multiple model checkpoints. Checkpoints can be either
specified manually or automatically chosen according to one of several
strategies. The default strategy of simply selecting the top-scoring N points
works well in practice.
"""

import argparse
import itertools
import os
from typing import Dict, Iterable, List

import mxnet as mx

from sockeye.log import setup_main_logger, log_sockeye_version
from . import arguments
from . import constants as C
from . import utils

logger = setup_main_logger(__name__, console=True, file_logging=False)


def __tmp6(__tmp0: Iterable[str]) :
    """
    Averages parameters from a list of .params file paths.

    :param param_paths: List of paths to parameter files.
    :return: Averaged parameter dictionary.
    """
    all_arg_params = []
    all_aux_params = []
    for path in __tmp0:
        logger.info("Loading parameters from '%s'", path)
        arg_params, aux_params = utils.load_params(path)
        all_arg_params.append(arg_params)
        all_aux_params.append(aux_params)

    logger.info("%d models loaded", len(all_arg_params))
    utils.check_condition(all(all_arg_params[0].keys() == p.keys() for p in all_arg_params),
                          "arg_param names do not match across models")
    utils.check_condition(all(all_aux_params[0].keys() == p.keys() for p in all_aux_params),
                          "aux_param names do not match across models")

    avg_params = {}
    # average arg_params
    for k in all_arg_params[0]:
        arrays = [p[k] for p in all_arg_params]
        avg_params["arg:" + k] = utils.average_arrays(arrays)
    # average aux_params
    for k in all_aux_params[0]:
        arrays = [p[k] for p in all_aux_params]
        avg_params["aux:" + k] = utils.average_arrays(arrays)

    return avg_params


def __tmp5(__tmp1: <FILL>, size=4, strategy="best", metric: str = C.PERPLEXITY) :
    """
    Finds N best points from .metrics file according to strategy.

    :param model_path: Path to model.
    :param size: Number of checkpoints to combine.
    :param strategy: Combination strategy.
    :param metric: Metric according to which checkpoints are selected.  Corresponds to columns in model/metrics file.
    :return: List of paths corresponding to chosen checkpoints.
    """
    __tmp3 = C.METRIC_MAXIMIZE[metric]
    __tmp8 = utils.get_validation_metric_points(__tmp1=__tmp1, metric=metric)
    # keep only points for which .param files exist
    param_path = os.path.join(__tmp1, C.PARAMS_NAME)
    __tmp8 = [(value, checkpoint) for value, checkpoint in __tmp8 if os.path.exists(param_path % checkpoint)]

    if strategy == "best":
        # N best scoring points
        top_n = _strategy_best(__tmp8, size, __tmp3)

    elif strategy == "last":
        # N sequential points ending with overall best
        top_n = _strategy_last(__tmp8, size, __tmp3)

    elif strategy == "lifespan":
        # Track lifespan of every "new best" point
        # Points dominated by a previous better point have lifespan 0
        top_n = __tmp7(__tmp8, size, __tmp3)
    else:
        raise RuntimeError("Unknown strategy, options: best last lifespan")

    # Assemble paths for params files corresponding to chosen checkpoints
    # Last element in point is always the checkpoint id
    params_paths = [
        os.path.join(__tmp1, C.PARAMS_NAME % point[-1]) for point in top_n
    ]

    # Report
    logger.info("Found: " + ", ".join(str(point) for point in top_n))

    return params_paths


def _strategy_best(__tmp8, size, __tmp3):
    top_n = sorted(__tmp8, reverse=__tmp3)[:size]
    return top_n


def _strategy_last(__tmp8, size, __tmp3):
    best = max if __tmp3 else min
    after_top = __tmp8.index(best(__tmp8)) + 1
    top_n = __tmp8[max(0, after_top - size):after_top]
    return top_n


def __tmp7(__tmp8, size, __tmp3):
    top_n = []
    cur_best = __tmp8[0]
    cur_lifespan = 0
    for point in __tmp8[1:]:
        better = point > cur_best if __tmp3 else point < cur_best
        if better:
            top_n.append(list(itertools.chain([cur_lifespan], cur_best)))
            cur_best = point
            cur_lifespan = 0
        else:
            top_n.append(list(itertools.chain([0], point)))
            cur_lifespan += 1
    top_n.append(list(itertools.chain([cur_lifespan], cur_best)))
    # Sort by lifespan, then by val
    top_n = sorted(
        top_n,
        key=lambda point: [point[0], point[1] if __tmp3 else -point[1]],
        reverse=True)[:size]
    return top_n


def main():
    """
    Commandline interface to average parameters.
    """
    params = argparse.ArgumentParser(description="Averages parameters from multiple models.")
    arguments.add_average_args(params)
    __tmp2 = params.parse_args()
    __tmp4(__tmp2)


def __tmp4(__tmp2: argparse.Namespace):
    log_sockeye_version(logger)

    if len(__tmp2.inputs) > 1:
        avg_params = __tmp6(__tmp2.inputs)
    else:
        __tmp0 = __tmp5(__tmp1=__tmp2.inputs[0],
                                       size=__tmp2.n,
                                       strategy=__tmp2.strategy,
                                       metric=__tmp2.metric)
        avg_params = __tmp6(__tmp0)

    mx.nd.save(__tmp2.output, avg_params)
    logger.info("Averaged parameters written to '%s'", __tmp2.output)


if __name__ == "__main__":
    main()
