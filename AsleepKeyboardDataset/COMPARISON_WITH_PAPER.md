# Comparison: Our Results vs. Original Paper

## Original Paper (Pearce et al., 2021)
- **Paper**: "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions"
- **Model**: GitHub Copilot (based on OpenAI Codex)
- **Result**: ~40% of generated code was vulnerable
- **Dataset**: 89 scenarios, 1,689 total programs generated

## Our Results
- **Model**: StarCoder-1B (much smaller than Codex)
- **Result**: 12.1% of generated code was vulnerable (164/1,350)
- **Dataset**: 54 DoW scenarios, 1,350 total programs generated (25 per scenario)
- **Temperature**: 0.6

## Key Differences Explaining Lower Vulnerability Rate

### 1. Different Models
- **Copilot/Codex**: Larger model, trained on all GitHub code (including vulnerable code)
- **StarCoder-1B**: Smaller model, potentially trained on more curated/recent data

### 2. Temporal Difference
- **Original study**: 2021 (early in AI coding assistant era)
- **Our study**: 2025 (models have learned from security research)

### 3. Prompt Context
Many of our prompts include security imports:
```python
from markupsafe import escape  # CWE-79 prompts
```
This biases the model toward secure completions.

### 4. Detection Methodology
- **Original paper**: Likely used more sophisticated vulnerability detection
- **Our approach**: Simple pattern matching may miss vulnerabilities

### 5. Scenario Selection
- We only tested DoW (Descriptive of Weakness) scenarios
- Original paper may have included more challenging scenarios

## Vulnerability Breakdown Comparison

### High Vulnerability Categories (Our Results)
- CWE-476 (NULL Pointer): 68.0%
- CWE-502 (Deserialization): 49.3%
- CWE-119 (Buffer Overflow): 40.0%

### Low Vulnerability Categories (Our Results)
- CWE-89 (SQL Injection): 10.7%
- CWE-78 (OS Command): 10.7%
- Many CWEs at 0%

## Why StarCoder Performs Better

1. **Training Data Evolution**: By 2024, there's more security-aware code in training datasets
2. **Security Research Impact**: Models trained after security studies like "Asleep at the Keyboard"
3. **Community Awareness**: More secure coding practices in open source
4. **Model Architecture**: StarCoder specifically designed for code generation

## Caveats

1. **Detection Limitations**: Our simple pattern matching may undercount vulnerabilities
2. **Scenario Bias**: Prompts with security imports bias toward secure code
3. **Sample Size**: We tested fewer scenarios (54 vs 89)
4. **Temperature Effect**: 0.6 may produce more conservative (safer) completions

## Conclusion

The 12.1% vs 40% difference likely reflects:
- Improved model training on security-aware code
- Temporal evolution of coding practices
- Differences in vulnerability detection methods
- Prompt context biasing

This suggests AI code generation has become more security-aware since 2021, but our simpler detection method may also contribute to the lower rate.