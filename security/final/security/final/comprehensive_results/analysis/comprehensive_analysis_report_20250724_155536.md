# Comprehensive SecLLMHolmes Baseline Experiment Report

**Experiment ID:** 20250724_155536
**Date:** 2025-07-24 15:55:52
**Models Tested:** bigcode/starcoderbase-1b
**Trials per Model:** 2
**Parameters:** Temperature=0.0, Top-p=1.0, Max Tokens=50

## Overall Performance Summary

| Model | Mean Accuracy | Std Dev | Trials |
|-------|---------------|---------|--------|
| starcoderbase-1b | 0.1667 | 0.0000 | 2 |

## Per-CWE Performance Analysis

### CWE-89 (SQL injection)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| starcoderbase-1b | 0.1667 | 0.0000 |

### CWE-79 (cross-site scripting)

| Model | Mean Accuracy | Std Dev |
|-------|---------------|---------|
| starcoderbase-1b | 0.1667 | 0.0000 |

## Key Findings

1. **Best Overall Performance:** starcoderbase-1b with 0.1667 accuracy
2. **Worst Overall Performance:** starcoderbase-1b with 0.1667 accuracy
3. **Performance Gap:** 0.0000 accuracy difference

### Best CWE Performance by Model

- **starcoderbase-1b:** CWE-89 (0.1667 accuracy)

## Statistical Significance

All results are based on 2 independent trials per model.
Standard deviations indicate variability across trials.

---
*Report generated on 2025-07-24 15:55:52*