# Comprehensive SecLLMHolmes Baseline Experiment Report

**Experiment ID:** 20250724_155718
**Date:** 2025-07-24 16:24:24
**Models Tested:** bigcode/starcoderbase-1b, bigcode/starcoderbase-7b, codellama/CodeLlama-7b-hf
**Trials per Model:** 3
**Parameters:** Temperature=0.0, Top-p=1.0, Max Tokens=200

## Overall Performance Summary

| Model | Mean Accuracy | Std Dev | Trials |
|-------|---------------|---------|--------|
| CodeLlama-7b-hf | 0.2708 | 0.0000 | 3 |
| starcoderbase-7b | 0.1250 | 0.0000 | 3 |
| starcoderbase-1b | 0.0625 | 0.0000 | 3 |

## Per-CWE Performance Analysis

### CWE-22 (path traversal)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| CodeLlama-7b-hf | 0.5000 | 0.0000 |
| starcoderbase-1b | 0.0000 | 0.0000 |
| starcoderbase-7b | 0.0000 | 0.0000 |

### CWE-77 (OS command injection)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| CodeLlama-7b-hf | 0.3333 | 0.0000 |
| starcoderbase-1b | 0.0000 | 0.0000 |
| starcoderbase-7b | 0.0000 | 0.0000 |

### CWE-79 (cross-site scripting)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| starcoderbase-7b | 0.5000 | 0.0000 |
| starcoderbase-1b | 0.1667 | 0.0000 |
| CodeLlama-7b-hf | 0.0000 | 0.0000 |

### CWE-89 (SQL injection)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| starcoderbase-7b | 0.5000 | 0.0000 |
| starcoderbase-1b | 0.1667 | 0.0000 |
| CodeLlama-7b-hf | 0.1667 | 0.0000 |

### CWE-190 (integer overflow)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| CodeLlama-7b-hf | 0.5000 | 0.0000 |
| starcoderbase-1b | 0.0000 | 0.0000 |
| starcoderbase-7b | 0.0000 | 0.0000 |

### CWE-416 (use after free)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| CodeLlama-7b-hf | 0.3333 | 0.0000 |
| starcoderbase-1b | 0.0000 | 0.0000 |
| starcoderbase-7b | 0.0000 | 0.0000 |

### CWE-476 (NULL pointer dereference)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| starcoderbase-1b | 0.0000 | 0.0000 |
| starcoderbase-7b | 0.0000 | 0.0000 |
| CodeLlama-7b-hf | 0.0000 | 0.0000 |

### CWE-787 (out-of-bounds write)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| CodeLlama-7b-hf | 0.3333 | 0.0000 |
| starcoderbase-1b | 0.1667 | 0.0000 |
| starcoderbase-7b | 0.0000 | 0.0000 |

## Key Findings

1. **Best Overall Performance:** CodeLlama-7b-hf with 0.2708 accuracy
2. **Worst Overall Performance:** starcoderbase-1b with 0.0625 accuracy
3. **Performance Gap:** 0.2083 accuracy difference

### Best CWE Performance by Model

- **starcoderbase-1b:** CWE-79 (0.1667 accuracy)
- **starcoderbase-7b:** CWE-79 (0.5000 accuracy)
- **CodeLlama-7b-hf:** CWE-22 (0.5000 accuracy)

## Statistical Significance

All results are based on 3 independent trials per model.
Standard deviations indicate variability across trials.

---
*Report generated on 2025-07-24 16:24:24*