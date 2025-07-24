# SecLLMHolmes Baseline Experiment Report

**Model:** bigcode/starcoderbase-1b
**Date:** 20250724_152606
**Configuration:** Temperature=0.0, Max Tokens=200

## Overall Performance

- **Accuracy:** 0.146 (14.6%)
- **Reasoning Score:** 0.060
- **Consistency:** 1.000

## Per-CWE Results

| CWE | Vulnerability Type | Accuracy | Reasoning | Consistency |
|-----|-------------------|----------|-----------|-------------|
| CWE-22 | Path Traversal | 0.000 | 0.118 | 1.000 |
| CWE-77 | Command Injection | 0.000 | 0.053 | 1.000 |
| CWE-79 | Cross-site Scripting | 0.333 | 0.079 | 1.000 |
| CWE-89 | SQL Injection | 0.500 | 0.082 | 1.000 |
| CWE-190 | Integer Overflow | 0.000 | 0.032 | 1.000 |
| CWE-416 | Use After Free | 0.167 | 0.016 | 1.000 |
| CWE-476 | NULL Pointer Dereference | 0.000 | 0.022 | 1.000 |
| CWE-787 | Out-of-bounds Write | 0.167 | 0.073 | 1.000 |

## Key Findings

1. **Overall Performance:** The model achieved 14.6% accuracy across all vulnerability types.
2. **Best Performance:** SQL Injection (CWE-89) with 0.5% accuracy.
3. **Worst Performance:** Path Traversal (CWE-22) with 0.0% accuracy.
4. **Consistency:** Model showed high consistency with 1.0 consistency rate.

## Recommendations

- Consider using larger models or implementing fine-tuning
- Improve prompt engineering for better vulnerability detection
- Implement neural steering techniques to improve security awareness
- Consider ensemble methods combining multiple models
