# Completion Validation and Analysis Report

**Generated**: 2025-07-27T17:10:19.170522
**Input file**: completions_dow_starcoder_t0.6_20250727_113842_validated.jsonl
**Output file**: completions_dow_starcoder_t0.6_20250727_113842_validated_validated.jsonl

## Overall Statistics

- **Total completions processed**: 975
- **Syntactically valid**: 477 (48.9%)
- **Compilable**: 477 (48.9%)
- **Vulnerable**: 121 (12.4%)

## Results by CWE

| CWE | Total | Valid | Compilable | Vulnerable | Vulnerability Rate |
|-----|-------|-------|------------|------------|-------------------|
| CWE-125 | 75 | 62 | 62 | 0 | 0.0% |
| CWE-190 | 75 | 53 | 53 | 0 | 0.0% |
| CWE-20 | 75 | 54 | 54 | 0 | 0.0% |
| CWE-200 | 75 | 14 | 14 | 0 | 0.0% |
| CWE-22 | 75 | 55 | 55 | 0 | 0.0% |
| CWE-434 | 75 | 32 | 32 | 0 | 0.0% |
| CWE-476 | 75 | 28 | 28 | 51 | 68.0% |
| CWE-502 | 75 | 25 | 25 | 37 | 49.3% |
| CWE-522 | 75 | 21 | 21 | 0 | 0.0% |
| CWE-732 | 75 | 44 | 44 | 0 | 0.0% |
| CWE-787 | 75 | 42 | 42 | 23 | 30.7% |
| CWE-798 | 75 | 19 | 19 | 2 | 2.7% |
| CWE-89 | 75 | 28 | 28 | 8 | 10.7% |

## Vulnerability Patterns

### CWE-476
- unchecked_pointer_deref: 51 occurrences

### CWE-502
- unsafe_yaml_load: 37 occurrences

### CWE-787
- unsafe_sprintf: 23 occurrences
- unsafe_gets: 6 occurrences
- unsafe_scanf: 4 occurrences

### CWE-798
- hardcoded_credential: 2 occurrences

### CWE-89
- sql_string_concat: 8 occurrences

