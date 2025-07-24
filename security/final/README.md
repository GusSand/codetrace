# SecLLMHolmes Baseline Experiment

This directory contains a comprehensive baseline experiment implementation that adapts SecLLMHolmes to work with the transformers library using StarCoder1B as the no-steering baseline for neural steering research.

## 🎯 Experiment Overview

**Objective**: Establish a no-steering baseline for SecLLMHolmes dataset using StarCoder1B with transformers library, providing a comparison point for neural steering experiments.

**Model**: `bigcode/starcoderbase-1b` (1.14B parameters)
**Dataset**: SecLLMHolmes hand-crafted vulnerability examples
**Generation Parameters**: 
- Temperature: 0.0 (deterministic, as recommended by paper)
- Top-p: 1.0
- Max new tokens: 200

## 📁 Files Structure

```
security/final/
├── baseline.py                    # Main baseline experiment implementation
├── test_baseline.py              # Quick test script to verify setup
├── analyze_baseline_results.py   # Comprehensive results analysis
├── README.md                     # This file
└── baseline_results/             # Generated results
    ├── baseline_results_*.json   # Raw experimental data
    └── analysis/                 # Analysis outputs
        ├── baseline_analysis.png # Performance visualizations
        └── baseline_summary_report.md # Comprehensive report
```

## 🚀 Key Features

### 1. **Complete SecLLMHolmes Integration**
- Automatically loads SecLLMHolmes dataset (hand-crafted, augmented, real-world)
- Handles all 8 CWE types: Path Traversal, Command Injection, XSS, SQL Injection, Integer Overflow, Use After Free, NULL Pointer Dereference, Out-of-bounds Write
- Proper ground truth evaluation using provided reasoning explanations

### 2. **Structured Output Parsing**
- Extracts Answer (yes/no/n/a) and Reason from generated text
- Uses regex patterns to identify security-related responses
- Handles model's natural language outputs robustly

### 3. **Comprehensive Evaluation Metrics**
- **Accuracy**: Compares extracted answer to ground truth vulnerability status
- **Reasoning Score**: Jaccard similarity between predicted and ground truth explanations  
- **Consistency**: Multiple trial consistency checking

### 4. **Paper-Compliant Generation**
- Uses exact parameters specified in SecLLMHolmes paper
- Deterministic generation (temperature=0.0) for reproducibility
- Proper tokenization and padding handling

## 📊 Baseline Results Summary

### Overall Performance
- **Accuracy**: 14.6% (Very Low)
- **Reasoning Score**: 0.060 (Poor) 
- **Consistency**: 100% (Highly Consistent)

### Per-CWE Performance
| CWE | Vulnerability Type | Accuracy | Key Finding |
|-----|-------------------|----------|-------------|
| CWE-89 | SQL Injection | 50.0% | Best performance |
| CWE-79 | Cross-site Scripting | 33.3% | Moderate detection |
| CWE-416 | Use After Free | 16.7% | Poor detection |
| CWE-787 | Out-of-bounds Write | 16.7% | Poor detection |
| CWE-22 | Path Traversal | 0.0% | Failed completely |
| CWE-77 | Command Injection | 0.0% | Failed completely |
| CWE-190 | Integer Overflow | 0.0% | Failed completely |  
| CWE-476 | NULL Pointer Dereference | 0.0% | Failed completely |

### Key Insights
- Model struggles with vulnerability detection (25% success on vulnerable code)
- Even worse at identifying secure code (4.2% success)  
- 70.8% of responses are ambiguous ("n/a")
- Clear room for improvement through neural steering

## 🔧 Usage Instructions

### 1. Run the Baseline Experiment
```bash
cd security/final
python baseline.py
```

### 2. Test Setup (Optional)
```bash
python test_baseline.py
```

### 3. Analyze Results
```bash
python analyze_baseline_results.py
```

## 📈 Integration with Neural Steering Research

This baseline provides the perfect foundation for neural steering experiments:

### For Paper Comparison
- Use the 14.6% accuracy as baseline comparison
- Compare steering improvements per CWE type
- Highlight specific areas where steering helps most (e.g., Path Traversal: 0% → X%)

### For Method Development
- Build on the structured output parsing
- Use the evaluation metrics framework
- Extend the CWE coverage for broader evaluation

### For Reproducibility
- All parameters match SecLLMHolmes paper specifications
- Deterministic generation ensures consistent baselines
- Comprehensive logging and result storage

## 🎯 Expected Neural Steering Improvements

Based on your previous research context, neural steering should improve:

1. **Security Pattern Recognition**: From 14.6% to target 40-60%
2. **CWE-Specific Detection**: Especially failed categories (Path Traversal, Command Injection)
3. **Reasoning Quality**: From 0.060 to higher semantic similarity
4. **Response Clarity**: Reduce ambiguous responses from 70.8%

## 🔍 Next Steps for Paper

1. **Extend to More Models**: Test with StarCoder-7B, CodeLlama variants
2. **Add Steering Experiments**: Apply your proven steering techniques
3. **Comparative Analysis**: Baseline vs. different steering intensities
4. **Real-world Evaluation**: Include augmented and real-world CWE examples

## 🛠 Technical Implementation Details

### Model Loading
- Uses `transformers.AutoModelForCausalLM`
- FP16 precision for memory efficiency
- Auto device mapping for multi-GPU setups

### Dataset Handling  
- Automatically discovers CWE examples
- Handles both vulnerable and patched versions
- Loads corresponding ground truth explanations

### Evaluation Framework
- Pattern-based answer extraction
- Keyword overlap reasoning scoring
- Statistical analysis with confidence intervals

---

**Ready for Neural Steering**: This baseline establishes the no-steering performance across all SecLLMHolmes vulnerability types, providing the perfect foundation for demonstrating neural steering improvements in your paper.

## 📚 References

Based on your neural steering research context and SecLLMHolmes paper:
- SecLLMHolmes: [arXiv:2312.12575](https://arxiv.org/abs/2312.12575)
- Your neural steering work: `chats/context/neural_steering_context_20250723_213701.md` 