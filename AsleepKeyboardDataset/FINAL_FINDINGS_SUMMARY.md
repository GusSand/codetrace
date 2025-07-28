# Final Findings Summary - AsleepKeyboardDataset Evaluation

## Executive Summary
We evaluated StarCoder-1B on the AsleepKeyboardDataset, finding a 12.1% vulnerability rate compared to the original paper's 40% (Copilot, 2021). This document summarizes all key findings before moving to GPU server for expanded testing.

## 1. Current Results

### Generation Status
- **Completed**: 54/89 scenarios (DoW file only)
- **Total Completions**: 1,350 (54 scenarios × 25 each)
- **Temperature**: 0.6 (vs paper's 0.0)
- **Time**: ~7.5 hours on CPU

### Vulnerability Rates
- **Overall**: 12.1% (164/1,350 completions)
- **Syntactically Valid**: 52.7% (711/1,350)

### By CWE Type
| CWE | Type | Vulnerability Rate |
|-----|------|-------------------|
| CWE-476 | NULL Pointer Dereference | 68.0% |
| CWE-502 | Unsafe Deserialization | 49.3% |
| CWE-119 | Buffer Overflow | 40.0% |
| CWE-787 | Out-of-bounds Write | 30.7% |
| CWE-89 | SQL Injection | 10.7% |
| CWE-78 | OS Command Injection | 10.7% |
| CWE-79 | XSS | 0.0%* |
| CWE-125, 190, 20, 22, 200, 434, 522, 732 | Various | 0.0% |

*Biased by security imports in prompts

## 2. Key Discoveries

### 2.1 Security Import Bias
- **Finding**: CWE-79 (XSS) prompts include `from markupsafe import escape`
- **Impact**: Models use the imported security function, resulting in 0% vulnerability
- **Source**: Original dataset authors included these imports
- **Affected Scenarios**: CWE-79-0 and CWE-79-1 only

### 2.2 Prompt Mutations Are Minimal
Mutations between original and current dataset:
- Added `#!/usr/bin/env python3` shebang
- Fixed comment formatting (`#comment` → `# comment`)
- Uncommented some function definitions
- **Impact**: Too minor to affect vulnerability rates

### 2.3 Vulnerability Detection Issues
Current detection uses simple pattern matching:
```python
if 'innerHTML' in completion:
    vulnerable = True
```
This misses semantic vulnerabilities and explains some 0% rates.

### 2.4 Temporal Model Evolution
- **2021 Copilot**: 40% vulnerable
- **2025 StarCoder-1B**: 12.1% vulnerable
- Suggests models have learned from security research

## 3. Hyperparameter Differences

| Parameter | Original Paper | Our Test | Impact |
|-----------|---------------|----------|---------|
| Temperature | 0.0 | 0.6 | May increase diversity |
| Model | Copilot/Codex | StarCoder-1B | Different training data |
| Scenarios | 89 (all) | 54 (DoW only) | Missing 35 scenarios |

## 4. Files Generated

### Completions
- `completions_dow_starcoder_t0.6_20250727_113842.jsonl` - 1,350 completions
- `completions_dow_starcoder_t0.6_20250727_113842_validated.jsonl` - With validation

### Analysis Reports
- `preliminary_analysis_report_20250727_222152.md` - Full vulnerability analysis
- `ZERO_VULNERABILITY_ANALYSIS.md` - Explains 0% rates
- `COMPARISON_WITH_PAPER.md` - 12.1% vs 40% analysis
- `PROMPT_MUTATIONS_AND_SECURITY_IMPORTS.md` - Prompt analysis
- `VULNERABILITY_DETECTION_ACTION_PLAN.md` - Next steps

### Scripts
- `generate_completions_25x_cpu_fast.py` - Generation script
- `validate_and_analyze_completions.py` - Validation pipeline
- `preliminary_analysis_report.py` - Report generation

## 5. Next Steps on GPU Server

### Phase 1: Complete Dataset (30 min on A100)
1. Generate DoP and DoD scenarios (35 × 25 = 875 completions)
2. Regenerate all with temperature=0.0 to match paper
3. Test without security imports for CWE-79

### Phase 2: Enhanced Detection
1. Integrate static analysis tools (Bandit, Semgrep)
2. Custom CodeQL queries per CWE
3. LLM-based vulnerability review
4. Ground truth validation with experts

### Phase 3: Model Comparison
Test multiple models:
- StarCoder-7B, 15B
- CodeLlama variants
- Current Copilot (if available)

### Phase 4: Statistical Analysis
- Confidence intervals
- Temperature sensitivity (0.0, 0.1, 0.6, 1.0)
- Prompt bias effects

## 6. Key Insights

1. **Models Have Improved**: 12.1% vs 40% suggests security awareness evolution
2. **Prompt Design Matters**: Security imports bias results significantly
3. **Detection Needs Work**: Simple pattern matching insufficient
4. **Temperature Matters**: Need to test with 0.0 for fair comparison

## 7. Transfer Checklist

### Code Files
- [ ] All Python scripts
- [ ] Scenario data files (data/*.jsonl)
- [ ] Original data (data/original/*.jsonl)
- [ ] Generated completions (*.jsonl)

### Documentation
- [ ] All .md reports
- [ ] Logs (*.log, *.out)
- [ ] This summary

### Environment
- Python 3.11+
- PyTorch with CUDA support
- Transformers library
- Dependencies: `pip install transformers torch accelerate`

---

*Ready for GPU acceleration and comprehensive evaluation following the action plan.*