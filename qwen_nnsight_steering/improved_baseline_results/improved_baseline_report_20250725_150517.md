# SecLLMHolmes Improved Baseline Test Results

**Date**: 2025-07-25 15:05:17

**Model**: Qwen/Qwen2.5-14B-Instruct

**Temperature**: 0.0


## Overall Performance

- **Accuracy**: 0.833 (83.3%)

- **Total Examples**: 18

- **Reasoning Quality**: 0.380


## Per-CWE Performance

| CWE | Description | Accuracy | Examples | Reasoning Quality |

|-----|-------------|----------|----------|-------------------|

| CWE-190 | Integer Overflow | 0.000 | 3 | 0.181 |

| CWE-22 | Path Traversal | 1.000 | 3 | 0.667 |

| CWE-416 | Use After Free | 1.000 | 3 | 0.347 |

| CWE-476 | NULL Pointer Dereference | 1.000 | 3 | 0.319 |

| CWE-77 | Command Injection | 1.000 | 3 | 0.417 |

| CWE-787 | Out-of-bounds Write | 1.000 | 3 | 0.347 |


## Performance Analysis

- **Best Performing CWE**: CWE-22 (1.000)

- **Most Challenging CWE**: CWE-190 (0.000)

- **Previous Baseline (Qwen2.5-14B-Instruct)**: 73.4%

- **Current Baseline**: 83.3%

- **Improvement**: +9.9%
