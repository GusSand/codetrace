# Sample Efficiency Experiment Results
Generated on: 2025-07-23 15:36:47

## Experiment Information
- Model: bigcode/starcoderbase-1b
- Timestamp: 2025-07-23T15:36:47.542326
- Total Experiments: 160
- Sample Counts: [0, 1, 3, 5, 10]
- Steering Scales: [1.0, 5.0, 10.0, 20.0]

## Key Findings
### 0 Samples per CVE
- Average Security Score: 0.018 ± 0.064
- Average Quality Score: 0.847 ± 0.195
- Improvement over Random: 1.00x

### 1 Samples per CVE
- Average Security Score: 0.004 ± 0.022
- Average Quality Score: 0.725 ± 0.268
- Improvement over Random: 0.21x

### 3 Samples per CVE
- Average Security Score: 0.000 ± 0.000
- Average Quality Score: 0.788 ± 0.263
- Improvement over Random: 0.00x

### 5 Samples per CVE
- Average Security Score: 0.008 ± 0.030
- Average Quality Score: 0.784 ± 0.271
- Improvement over Random: 0.43x

### 10 Samples per CVE
- Average Security Score: 0.000 ± 0.000
- Average Quality Score: 0.791 ± 0.255
- Improvement over Random: 0.00x

## Best Configurations by Sample Count
### 0 Samples
- Best Security Score: 0.333
- Optimal Scale: 5.0
- Optimal Layers: [7, 12, 16]

### 1 Samples
- Best Security Score: 0.125
- Optimal Scale: 5.0
- Optimal Layers: [7, 12, 16]

### 3 Samples
- Best Security Score: 0.000
- Optimal Scale: 1.0
- Optimal Layers: [4, 12, 20]

### 5 Samples
- Best Security Score: 0.125
- Optimal Scale: 10.0
- Optimal Layers: [4, 12, 20]

### 10 Samples
- Best Security Score: 0.000
- Optimal Scale: 1.0
- Optimal Layers: [4, 12, 20]

## Recommendations
1. Optimal sample count: 5 samples per CVE (improvement: 0.43x)
2. Diminishing returns after 1 samples (gain: -0.214)

## Sample Efficiency Analysis

| Samples | Security Score | Improvement | Quality Score |
|---------|----------------|-------------|---------------|
| 0 | 0.018 | 1.00x | 0.847 |
| 1 | 0.004 | 0.21x | 0.725 |
| 3 | 0.000 | 0.00x | 0.788 |
| 5 | 0.008 | 0.43x | 0.784 |
| 10 | 0.000 | 0.00x | 0.791 |

---
*This report was generated automatically by the Sample Efficiency Experiment*