# Steering Strength Experiments

This directory contains comprehensive experiments to test different steering strengths and layer configurations for security steering in Large Language Models.

## 🎯 **Experiment Overview**

The experiments test **reasonable steering strengths** (5.0, 10.0, 20.0) instead of the extremely high value of 100.0 used previously. This aligns better with typical steering literature which uses values between 0.1-5.0.

## 🔧 **Key Fixes Applied**

### 1. **Logging Path Fix**
- **Problem**: Log files were being created in nested `security/security/` directories
- **Solution**: Created proper `security/logs/` directory structure
- **Code**: 
```python
# Create logs directory if it doesn't exist
log_dir = Path("security/logs")
log_dir.mkdir(exist_ok=True)
```

### 2. **Comprehensive Tracing**
- **Problem**: Limited debugging capabilities
- **Solution**: Added `TracingLogger` class with performance tracking, memory monitoring, and detailed error reporting
- **Features**:
  - Function execution time tracking
  - Memory usage monitoring
  - Detailed error logging with stack traces
  - Tensor information logging
  - Model information logging

### 3. **Decorator Pattern Implementation**
- **Problem**: Decorator syntax was incorrect
- **Solution**: Implemented proper decorator pattern for tracing:
```python
def create_security_examples(self) -> Tuple[List[str], List[str]]:
    return self.logger.trace_function("create_security_examples")(self._create_security_examples)()

def _create_security_examples(self) -> Tuple[List[str], List[str]]:
    # Actual implementation
```

## 📊 **Experiment Configuration**

### **Steering Strengths Tested**
- `5.0` - Low steering (literature typical)
- `10.0` - Medium steering  
- `20.0` - High steering (still reasonable)

### **Layer Configurations Tested**
- `[4]` - Single early layer
- `[8]` - Single middle layer
- `[12]` - Single late layer
- `[4, 8]` - Two layers (early-middle)
- `[8, 12]` - Two layers (middle-late)
- `[4, 8, 12]` - Three layers (distributed)

### **Vulnerability Types**
- SQL Injection (CWE-89)
- Cross-Site Scripting/XSS (CWE-79)
- Path Traversal (CWE-22)
- Command Injection (CWE-78)

## 🚀 **How to Run Experiments**

### **1. Test Setup (Recommended First Step)**
```bash
cd /home/paperspace/dev/codetrace
python security/test_steering_experiment.py
```
This verifies that all components work correctly before running the full experiment.

### **2. Run Full Experiment**
```bash
cd /home/paperspace/dev/codetrace
python security/run_steering_experiment.py
```
This runs the complete experiment with all steering strengths and layer configurations.

### **3. Visualize Results**
```bash
cd /home/paperspace/dev/codetrace
python security/visualize_steering_strength.py --results-file steering_strength_results_YYYYMMDD_HHMMSS.json
```

## 📁 **Output Files**

### **Experiment Results**
- `steering_strength_results_YYYYMMDD_HHMMSS.json` - Raw experiment data
- `steering_strength_analysis_YYYYMMDD_HHMMSS.json` - Analysis results

### **Logs**
- `security/logs/steering_experiment_YYYYMMDD_HHMMSS.log` - Detailed experiment logs
- `security/logs/visualization_YYYYMMDD_HHMMSS.log` - Visualization logs

### **Visualizations**
- `security/report/visualizations/steering_scale_analysis.png`
- `security/report/visualizations/layer_config_analysis.png`
- `security/report/visualizations/vulnerability_analysis.png`
- `security/report/visualizations/performance_analysis.png`
- `security/report/visualizations/combined_analysis.png`
- `security/report/visualizations/heatmap_analysis.png`
- `security/report/visualizations/experiment_summary_report.md`

## 🔍 **Tracing and Debugging Features**

### **Performance Tracking**
- Function execution times
- Memory usage before/after operations
- Generation statistics
- Error tracking with full stack traces

### **Detailed Logging**
- Model loading and configuration
- Tensor shapes and properties
- Steering vector creation process
- Generation step-by-step progress
- Evaluation results

### **Error Handling**
- Graceful failure recovery
- Retry mechanisms
- Detailed error reporting
- Memory cleanup

## 📈 **Expected Results**

Based on literature and previous experiments, we expect:

1. **Steering Scale Effects**:
   - Scale 5.0: Moderate security improvement, minimal quality impact
   - Scale 10.0: Good security improvement, some quality trade-off
   - Scale 20.0: High security improvement, potential quality degradation

2. **Layer Configuration Effects**:
   - Single layers: Faster generation, focused steering
   - Multiple layers: More comprehensive steering, slower generation
   - Middle layers (8, 12): Most effective for security patterns

3. **Vulnerability-Specific Results**:
   - SQL Injection: High improvement with parameterized query patterns
   - XSS: Moderate improvement with HTML escaping
   - Path Traversal: Good improvement with safe path handling
   - Command Injection: High improvement with subprocess safety

## 🛠️ **Troubleshooting**

### **Common Issues**

1. **Model Loading Errors**:
   - Check internet connection for model download
   - Verify model name is correct
   - Check available GPU memory

2. **Memory Issues**:
   - Reduce `max_new_tokens` in config
   - Use smaller model (e.g., `bigcode/starcoder2-1b` or `codellama/CodeLlama-7b-hf`)
   - Reduce number of layer configurations

3. **Generation Timeouts**:
   - Increase `timeout_seconds` in config
   - Reduce `max_new_tokens`
   - Check system resources

### **Debug Mode**
All scripts run with `debug_mode=True` by default, providing detailed logging. Check the log files in `security/logs/` for troubleshooting information.

## 📚 **Technical Details**

### **Steering Vector Construction**
The experiments use contextual embedding-based steering vectors:
1. Extract hidden states from secure vs insecure code examples
2. Compute difference vectors for each layer
3. Apply steering vectors during generation with specified scale

### **Evaluation Metrics**
- **Security Score**: Presence of secure patterns, absence of vulnerable patterns
- **Quality Score**: Code coherence, repetition, syntactic correctness  
- **Match Score**: Similarity to expected secure code
- **Generation Time**: Performance measurement
- **Memory Usage**: Resource consumption tracking

### **Model Architecture**
- Uses `nnsight` library for model interpretation
- Applies steering to specific transformer layers
- Modifies hidden states during generation process
- Supports multiple layer configurations simultaneously

## 🤝 **Contributing**

When modifying the experiments:
1. Test changes with `test_steering_experiment.py` first
2. Add appropriate tracing to new functions
3. Update this README with new features
4. Ensure all error handling includes detailed logging

## 📄 **License**

This code is part of the CodeTrace project for security steering research. 