# AsleepKeyboardDataset Full Evaluation Report (CPU-Only)

**Generated**: 2025-07-27T08:05:46.144152
**Model**: bigcode/starcoderbase-1b
**Device**: CPU
**Total Scenarios**: 89
**Completed Scenarios**: 89
**Errors**: 0

## Overall Results

- **Total Evaluated**: 89
- **Vulnerable**: 58
- **Secure**: 31
- **Vulnerability Rate**: 65.2%

## Results by CWE Type

| CWE | Total | Vulnerable | Rate | Most Common Pattern |
|-----|-------|------------|------|---------------------|
| CWE-502 | 3 | 3 | 100.0% | unsafe_yaml |
| CWE-190 | 3 | 3 | 100.0% | no_security |
| CWE-522 | 3 | 3 | 100.0% | no_security |
| CWE-125 | 3 | 3 | 100.0% | no_security |
| CWE-200 | 3 | 3 | 100.0% | no_security |
| CWE-476 | 3 | 3 | 100.0% | unchecked_deref |
| CWE-787 | 3 | 3 | 100.0% | no_security |
| CWE-78 | 3 | 3 | 100.0% | no_security |
| CWE-119 | 3 | 3 | 100.0% | no_security |
| CWE-306 | 3 | 3 | 100.0% | no_security |
| CWE-1271 | 3 | 3 | 100.0% | no_security |
| CWE-1234 | 3 | 3 | 100.0% | no_security |
| CWE-1294 | 3 | 3 | 100.0% | no_security |
| CWE-1242 | 3 | 3 | 100.0% | no_security |
| CWE-1245 | 3 | 3 | 100.0% | no_security |
| CWE-20 | 3 | 2 | 66.7% | no_security |
| CWE-22 | 3 | 2 | 66.7% | no_security |
| CWE-434 | 3 | 2 | 66.7% | no_security |
| CWE-732 | 3 | 2 | 66.7% | no_security |
| CWE-416 | 3 | 2 | 66.7% | no_security |
| CWE-798 | 3 | 1 | 33.3% | has_validation |
| CWE-89 | 20 | 2 | 10.0% | parameterized |
| CWE-79 | 3 | 0 | 0.0% | has_validation |
| CWE-1254 | 3 | 0 | 0.0% | has_validation |

## Key Findings

### Most Vulnerable CWEs (>80% vulnerability rate):
- **CWE-502**: 100.0% (3/3)
- **CWE-190**: 100.0% (3/3)
- **CWE-522**: 100.0% (3/3)
- **CWE-125**: 100.0% (3/3)
- **CWE-200**: 100.0% (3/3)
- **CWE-476**: 100.0% (3/3)
- **CWE-787**: 100.0% (3/3)
- **CWE-78**: 100.0% (3/3)
- **CWE-119**: 100.0% (3/3)
- **CWE-306**: 100.0% (3/3)
- **CWE-1271**: 100.0% (3/3)
- **CWE-1234**: 100.0% (3/3)
- **CWE-1294**: 100.0% (3/3)
- **CWE-1242**: 100.0% (3/3)
- **CWE-1245**: 100.0% (3/3)

### Most Secure CWEs (<20% vulnerability rate):
- **CWE-89**: 10.0% (2/20)
- **CWE-79**: 0.0% (0/3)
- **CWE-1254**: 0.0% (0/3)

## Vulnerability Patterns

### Most Common Vulnerability Patterns:
- no_security: 50 occurrences
- parameterized: 17 occurrences
- has_validation: 14 occurrences
- unsafe_yaml: 3 occurrences
- unchecked_deref: 2 occurrences
- unsafe_sprintf: 1 occurrences
- subprocess_shell: 1 occurrences
- unsafe_strcpy: 1 occurrences

## Evaluation Metadata

- Start Time: 2025-07-27T07:57:20.642658
- End Time: 2025-07-27T08:05:46.144218
- Total Errors: 0
- Device Used: CPU (MPS bypassed)

## Conclusion

The full evaluation of 89 scenarios shows an overall vulnerability rate of 65.2%. This comprehensive analysis provides definitive evidence about the current state of the AsleepKeyboardDataset.

### Key Takeaways:

1. **Dataset Difficulty**: With a 65.2% vulnerability rate, the dataset remains challenging for current models.

2. **CWE Variation**: Vulnerability rates vary across different CWE types, from 0.0% to 100.0%.

3. **Pattern Analysis**: The most common vulnerability patterns provide insights into what security issues models struggle with most.

4. **Performance**: Evaluation completed on CPU to bypass MPS compatibility issues. While slower, this ensures complete and accurate results.

---

*This report represents a complete evaluation of all available scenarios in the AsleepKeyboardDataset using CPU processing.*
