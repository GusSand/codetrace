# SecLLMHolmes Direct Baseline Test Results

**Date**: 2025-07-25 14:59:12

**Model**: Qwen/Qwen2.5-14B-Instruct

**Temperature**: 0.0


## Overall Performance

- **Accuracy**: 0.056 (5.6%)

- **Total Examples**: 18

- **Reasoning Quality**: 0.380


## Per-CWE Performance

| CWE | Description | Accuracy | Examples | Reasoning Quality |

|-----|-------------|----------|----------|-------------------|

| CWE-190 | Integer Overflow | 0.000 | 3 | 0.181 |

| CWE-22 | Path Traversal | 0.000 | 3 | 0.667 |

| CWE-416 | Use After Free | 0.333 | 3 | 0.347 |

| CWE-476 | NULL Pointer Dereference | 0.000 | 3 | 0.319 |

| CWE-77 | Command Injection | 0.000 | 3 | 0.417 |

| CWE-787 | Out-of-bounds Write | 0.000 | 3 | 0.347 |


## Performance Analysis

- **Best Performing CWE**: CWE-416 (0.333)

- **Most Challenging CWE**: CWE-22 (0.000)

- **Previous Baseline (Qwen2.5-14B-Instruct)**: 73.4%

- **Current Baseline**: 5.6%

- **Difference**: -67.8%
