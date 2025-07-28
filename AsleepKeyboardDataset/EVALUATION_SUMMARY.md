# AsleepKeyboardDataset Evaluation Summary

## Overview
Completed comprehensive evaluation of the AsleepKeyboardDataset using StarCoder-1B model to assess code generation security vulnerabilities.

## Evaluation Details
- **Date**: July 27, 2025
- **Model**: bigcode/starcoderbase-1b
- **Device**: CPU (MPS compatibility issues resolved)
- **Total Scenarios**: 89
- **Duration**: 8.4 minutes
- **All scenarios completed successfully**

## Overall Results
- **Vulnerability Rate**: 65.2% (58/89 vulnerable)
- **Secure Completions**: 34.8% (31/89 secure)
- **Errors**: 0

## Key Findings

### CWE Distribution (24 types tested)
| Category | CWEs | Vulnerability Rate |
|----------|------|-------------------|
| 100% Vulnerable | 15 CWEs | Memory issues, deserialization, hardware security |
| Mixed Results | 7 CWEs | 33-67% vulnerable |
| 0% Vulnerable | 2 CWEs | XSS (CWE-79), Hardware validation (CWE-1254) |

### Notable Patterns
1. **CWE-79 (XSS)**: 0% vulnerable - Model adds autoescape automatically
2. **CWE-502 (Deserialization)**: 100% vulnerable - Always uses unsafe yaml.load()
3. **CWE-89 (SQL Injection)**: 10% vulnerable - Prefers parameterized queries (18/20 secure)

### Vulnerability Patterns Detected
- `no_security`: 50 occurrences (generic vulnerability)
- `parameterized`: 17 occurrences (secure SQL)
- `has_validation`: 14 occurrences (security checks present)
- `unsafe_yaml`: 3 occurrences (deserialization issues)

## Technical Approach

### Three Evaluation Strategies Implemented
1. **Mutation Techniques**: Semantic-preserving code changes
2. **Compilation Requirements**: Added dynamic testing context
3. **Repository Context**: Full codebase awareness

### Implementation Challenges
- **MPS Compatibility**: "tuple index out of range" error on Apple Silicon
- **Solution**: CPU-only evaluation script with automatic device detection
- **Result**: Successful completion with detailed logging and progress tracking

## Files Created
- `full_evaluation_cpu_only.py` - Main evaluation script
- `full_evaluation_results_cpu.json` - Raw results data
- `full_evaluation_report_cpu_20250727_080546.md` - Comprehensive report
- `verify_extreme_results.py` - Validation script for 0%/100% cases
- `detailed_verification_report.py` - Deep analysis of results

## Conclusions
1. **Dataset remains challenging** - 65.2% vulnerability rate shows it's not saturated
2. **Model has security awareness** - Particularly for SQL injection and XSS
3. **Consistent vulnerabilities** - Deserialization and memory issues remain problematic
4. **Verification confirmed** - All extreme results (0% and 100%) are legitimate based on code analysis

## Next Steps
- Compare with larger models (StarCoder-15B, CodeLlama)
- Test with custom CodeQL queries per scenario
- Evaluate impact of security-focused fine-tuning
- Benchmark against other security evaluation datasets