# Working Steering vs Baseline Experiment Results

**Date**: 2025-07-25 16:31:25

**Model**: Qwen/Qwen2.5-1.5B-Instruct

**Steering Strength**: 10.0

**Target Layers**: [12, 24, 36, 47]


## Overall Performance Comparison

| Experiment | Accuracy | Examples | Reasoning Quality |

|------------|----------|----------|-------------------|

| **baseline** | **0.333** | **18** | **0.178** |

| steering_cwe-22 | 0.333 (+0.000) | 3 | 0.250 |

| steering_cwe-77 | 0.333 (+0.000) | 3 | 0.153 |

| steering_cwe-190 | 0.000 (-0.333) | 3 | 0.083 |

| steering_cwe-476 | 0.000 (-0.333) | 3 | 0.042 |


## Per-CWE Performance Analysis

| CWE | Baseline | Steering | Improvement |

|-----|----------|----------|-------------|

| CWE-190 | 0.000 | 0.000 | +0.000 |

| CWE-22 | 0.667 | 0.333 | -0.333 |

| CWE-416 | 1.000 | 0.000 | -1.000 |

| CWE-476 | 0.000 | 0.000 | +0.000 |

| CWE-77 | 0.333 | 0.000 | -0.333 |

| CWE-787 | 0.000 | 0.000 | +0.000 |


## Key Findings

- **Baseline Accuracy**: 0.000

- **Best Steering Accuracy**: 0.333

- **Overall Improvement**: +0.333 (+33.3%)

- **Most Improved CWE**: CWE-190 (+0.000)

- **Least Improved CWE**: CWE-416 (-1.000)
