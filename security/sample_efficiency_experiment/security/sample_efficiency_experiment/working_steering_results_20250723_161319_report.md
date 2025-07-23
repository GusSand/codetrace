# Working Steering Sample Efficiency Experiment Results
Generated on: 2025-07-23 16:13:19

## Experiment Information
- Model: bigcode/starcoderbase-1b
- Timestamp: 2025-07-23T16:13:19.877203
- Total Experiments: 20
- Sample Counts: [0, 1, 3, 5, 10]
- Steering Scales: [20.0]
- Experiment Type: working_steering

## Key Findings
### 0 Samples per CVE
- Average Security Score: 0.000 ± 0.000
- Average Quality Score: 0.275 ± 0.179
- Improvement over Random: 1.00x

### 1 Samples per CVE
- Average Security Score: 0.000 ± 0.000
- Average Quality Score: 0.800 ± 0.212
- Improvement over Random: 1.00x

### 3 Samples per CVE
- Average Security Score: 0.000 ± 0.000
- Average Quality Score: 0.500 ± 0.200
- Improvement over Random: 1.00x

### 5 Samples per CVE
- Average Security Score: 0.031 ± 0.054
- Average Quality Score: 0.350 ± 0.350
- Improvement over Random: 0.03x

### 10 Samples per CVE
- Average Security Score: 0.000 ± 0.000
- Average Quality Score: 0.400 ± 0.100
- Improvement over Random: 1.00x

## Best Configurations by Sample Count
### 0 Samples
- Best Security Score: 0.000
- Optimal Scale: 20.0
- Optimal Layers: [4, 12, 20]

### 1 Samples
- Best Security Score: 0.000
- Optimal Scale: 20.0
- Optimal Layers: [4, 12, 20]

### 3 Samples
- Best Security Score: 0.000
- Optimal Scale: 20.0
- Optimal Layers: [4, 12, 20]

### 5 Samples
- Best Security Score: 0.125
- Optimal Scale: 20.0
- Optimal Layers: [4, 12, 20]

### 10 Samples
- Best Security Score: 0.000
- Optimal Scale: 20.0
- Optimal Layers: [4, 12, 20]

## Recommendations
1. Optimal sample count: 1 samples per CVE (improvement: 1.00x)
2. Diminishing returns after 1 samples (gain: 0.000)

## Sample Efficiency Analysis

| Samples | Security Score | Improvement | Quality Score |
|---------|----------------|-------------|---------------|
| 0 | 0.000 | 1.00x | 0.275 |
| 1 | 0.000 | 1.00x | 0.800 |
| 3 | 0.000 | 1.00x | 0.500 |
| 5 | 0.031 | 0.03x | 0.350 |
| 10 | 0.000 | 1.00x | 0.400 |

---
*This report was generated automatically by the Working Steering Sample Efficiency Experiment*