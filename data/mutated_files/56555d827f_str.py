from typing import TypeAlias
__typ0 : TypeAlias = "DistributionMatchingGenerator"
import datetime
import json
import logging
from collections import OrderedDict
from typing import List, Dict, Any

import guacamol
from guacamol.distribution_learning_benchmark import DistributionLearningBenchmark, DistributionLearningBenchmarkResult
from guacamol.distribution_matching_generator import DistributionMatchingGenerator
from guacamol.benchmark_suites import distribution_learning_benchmark_suite
from guacamol.utils.data import get_time_string

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def __tmp7(__tmp1: __typ0,
                                 __tmp5: str,
                                 __tmp4='output_distribution_learning.json',
                                 __tmp0='v1') :
    """
    Assesses a distribution-matching model for de novo molecule design.

    Args:
        model: Model to evaluate
        chembl_training_file: path to ChEMBL training set, necessary for some benchmarks
        json_output_file: Name of the file where to save the results in JSON format
        benchmark_version: which benchmark suite to execute
    """
    __tmp6(__tmp1=__tmp1,
                                  __tmp5=__tmp5,
                                  __tmp4=__tmp4,
                                  __tmp0=__tmp0,
                                  __tmp2=10000)


def __tmp6(__tmp1: __typ0,
                                  __tmp5: str,
                                  __tmp4: <FILL>,
                                  __tmp0,
                                  __tmp2: int) -> None:
    """
    Internal equivalent to assess_distribution_learning, but allows for a flexible number of samples.
    To call directly only for testing.
    """
    logger.info(f'Benchmarking distribution learning, version {__tmp0}')
    benchmarks = distribution_learning_benchmark_suite(chembl_file_path=__tmp5,
                                                       version_name=__tmp0,
                                                       __tmp2=__tmp2)

    results = __tmp3(__tmp1=__tmp1, benchmarks=benchmarks)

    benchmark_results: Dict[str, Any] = OrderedDict()
    benchmark_results['guacamol_version'] = guacamol.__version__
    benchmark_results['benchmark_suite_version'] = __tmp0
    benchmark_results['timestamp'] = get_time_string()
    benchmark_results['samples'] = __tmp1.generate(100)
    benchmark_results['results'] = [vars(result) for result in results]

    logger.info(f'Save results to file {__tmp4}')
    with open(__tmp4, 'wt') as f:
        f.write(json.dumps(benchmark_results, indent=4))


def __tmp3(__tmp1,
                                               benchmarks: List[DistributionLearningBenchmark]
                                               ) -> List[DistributionLearningBenchmarkResult]:
    """
    Evaluate a model with the given benchmarks.
    Should not be called directly except for testing purposes.

    Args:
        model: model to assess
        benchmarks: list of benchmarks to evaluate
        json_output_file: Name of the file where to save the results in JSON format
    """

    logger.info(f'Number of benchmarks: {len(benchmarks)}')

    results = []
    for i, benchmark in enumerate(benchmarks, 1):
        logger.info(f'Running benchmark {i}/{len(benchmarks)}: {benchmark.name}')
        result = benchmark.assess_model(__tmp1)
        logger.info(f'Results for the benchmark "{result.benchmark_name}":')
        logger.info(f'  Score: {result.score:.6f}')
        logger.info(f'  Sampling time: {str(datetime.timedelta(seconds=int(result.sampling_time)))}')
        logger.info(f'  Metadata: {result.metadata}')
        results.append(result)

    logger.info('Finished execution of the benchmarks')

    return results
