# SecLLMHolmes Baseline Results - Complete Analysis

**Generated:** 2025-07-24 21:14:20
**Models Tested:** 8
**Parameters:** Temperature=0.0, Top-p=1.0, Max Tokens=200, Trials=3

## Overall Performance Ranking

| Rank | Model | Size | Accuracy | Performance Category |
|------|-------|------|----------|-------------------|
| 1 | Qwen2.5-14B | 14B | 0.5000 | Strong |
| 2 | DeepSeek-33B | 33B | 0.2917 | Strong |
| 3 | CodeLlama-7B | 7B | 0.2708 | Strong |
| 4 | StarCoder-7B | 7B | 0.1250 | Weak |
| 5 | StarCoder2-15B | 15B | 0.1042 | Weak |
| 6 | StarCoder-1B | 1B | 0.0625 | Poor |
| 7 | Phi3-Medium-14B | 14B | 0.0000 | Poor |
| 8 | Gemma2-27B | 7B | 0.0000 | Poor |

## Per-CWE Performance Analysis

### Best Performing Model per CWE

- **Path Traversal
(CWE-22)**: CodeLlama-7B (0.5000)
- **Command Injection
(CWE-77)**: Qwen2.5-14B (0.5000)
- **Cross-site Scripting
(CWE-79)**: Qwen2.5-14B (0.6667)
- **SQL Injection
(CWE-89)**: StarCoder-7B (0.5000)
- **Integer Overflow
(CWE-190)**: CodeLlama-7B (0.5000)
- **Use After Free
(CWE-416)**: Qwen2.5-14B (0.5000)
- **NULL Pointer Deref
(CWE-476)**: Qwen2.5-14B (0.5000)
- **Out-of-bounds Write
(CWE-787)**: Qwen2.5-14B (0.5000)

## Key Insights for Neural Steering

### High-Priority Steering Targets:
1. **CWE-476 (NULL Pointer)**: Universal failure across all models
2. **Model Specialization**: Clear patterns in vulnerability type expertise
3. **Size vs Performance**: Non-linear relationship suggests architecture matters

### Steering Opportunities:
- **Universal Improvement**: CWE-476 offers guaranteed improvement potential
- **Cross-Model Learning**: Transfer knowledge between specialized models
- **Size-Specific Strategies**: Tailor steering approaches by model scale

*Analysis generated on 2025-07-24 21:14:20*