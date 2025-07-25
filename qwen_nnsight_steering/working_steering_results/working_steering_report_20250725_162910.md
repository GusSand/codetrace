# Working Steering vs Baseline Experiment Results

**Date**: 2025-07-25 16:29:10

**Model**: Qwen/Qwen2.5-1.5B-Instruct

**Steering Strength**: 10.0

**Target Layers**: [12, 24, 36, 47]


## Overall Performance Comparison

| Experiment | Accuracy | Examples | Reasoning Quality |

|------------|----------|----------|-------------------|

| **baseline** | **0.333** | **6** | **0.188** |

| steering_cwe-22 | 0.000 (-0.333) | 1 | 0.250 |

| steering_cwe-77 | 1.000 (+0.667) | 1 | 0.333 |

| steering_cwe-190 | 0.000 (-0.333) | 1 | 0.125 |

| steering_cwe-476 | 0.000 (-0.333) | 1 | 0.083 |


## Per-CWE Performance Analysis

| CWE | Baseline | Steering | Improvement |

|-----|----------|----------|-------------|

| CWE-190 | 0.000 | 0.000 | +0.000 |

| CWE-22 | 1.000 | 0.000 | -1.000 |

| CWE-416 | 1.000 | 0.000 | -1.000 |

| CWE-476 | 0.000 | 0.000 | +0.000 |

| CWE-77 | 0.000 | 0.000 | +0.000 |

| CWE-787 | 0.000 | 0.000 | +0.000 |


## Key Findings

- **Baseline Accuracy**: 0.000

- **Best Steering Accuracy**: 1.000

- **Overall Improvement**: +1.000 (+100.0%)

- **Most Improved CWE**: CWE-77 (+0.000)

- **Least Improved CWE**: CWE-22 (-1.000)
