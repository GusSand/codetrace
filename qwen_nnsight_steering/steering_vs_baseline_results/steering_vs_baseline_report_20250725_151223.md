# Steering vs Baseline Experiment Results

**Date**: 2025-07-25 15:12:23

**Model**: Qwen/Qwen2.5-14B-Instruct

**Steering Strength**: 20.0


## Overall Performance Comparison

| Experiment | Accuracy | Examples | Reasoning Quality |

|------------|----------|----------|-------------------|

| **baseline** | **0.833** | **18** | **0.380** |

| steering_cwe-22 | 1.000 (+0.167) | 3 | 0.667 |

| steering_cwe-77 | 1.000 (+0.167) | 3 | 0.417 |

| steering_cwe-190 | 0.000 (-0.833) | 3 | 0.181 |

| steering_cwe-476 | 1.000 (+0.167) | 3 | 0.319 |


## Per-CWE Performance Analysis

| CWE | Baseline | Steering | Improvement |

|-----|----------|----------|-------------|

| CWE-190 | 0.000 | 0.000 | +0.000 |

| CWE-22 | 1.000 | 1.000 | +0.000 |

| CWE-416 | 1.000 | 0.000 | -1.000 |

| CWE-476 | 1.000 | 0.000 | -1.000 |

| CWE-77 | 1.000 | 0.000 | -1.000 |

| CWE-787 | 1.000 | 0.000 | -1.000 |


## Key Findings

- **Baseline Accuracy**: 1.000

- **Best Steering Accuracy**: 1.000

- **Overall Improvement**: +0.000 (+0.0%)

- **Most Improved CWE**: CWE-22 (+0.000)

- **Least Improved CWE**: CWE-77 (-1.000)
