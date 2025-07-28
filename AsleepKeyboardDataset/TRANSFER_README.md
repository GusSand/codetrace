# Transfer Instructions - AsleepKeyboardDataset to GPU Server

## Quick Start on GPU Server

```bash
# 1. Clone/copy this directory to GPU server
scp -r AsleepKeyboardDataset/ user@gpu-server:/path/

# 2. Set up environment
conda create -n asleep python=3.11
conda activate asleep
pip install torch transformers accelerate pandas matplotlib

# 3. Verify GPU
python -c "import torch; print(torch.cuda.is_available())"

# 4. Continue generation with temp=0
python generate_completions_gpu.py --temperature 0.0 --scenarios all
```

## Key Files to Transfer

### Essential Scripts
1. `generate_completions_25x_cpu_fast.py` - Modify for GPU
2. `validate_and_analyze_completions.py` - Validation pipeline
3. `preliminary_analysis_report.py` - Report generation

### Data Files
1. `data/scenario_*.jsonl` - All 89 scenarios
2. `data/original/*.jsonl` - Original unmutated prompts
3. `completions_dow_starcoder_t0.6_*.jsonl` - Current results

### Documentation
1. `VULNERABILITY_DETECTION_ACTION_PLAN.md` - Your roadmap
2. `FINAL_FINDINGS_SUMMARY.md` - Current status
3. All other .md files for reference

## GPU Optimization Tips

### Model Loading
```python
# Use GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(
    "bigcode/starcoderbase-1b",
    torch_dtype=torch.float16,  # Use fp16 on GPU
    device_map="auto"
).to(device)
```

### Batch Processing
```python
# A100 can handle larger batches
batch_size = 8  # or even 16
```

## Priority Tasks

1. **Complete Missing Scenarios**
   - DoP: 17 scenarios
   - DoD: 18 scenarios
   - Total: 875 completions needed

2. **Temperature 0.0 Testing**
   - Regenerate all 89 scenarios with temp=0
   - Matches original paper

3. **Remove Security Imports**
   - Test CWE-79 without `from markupsafe import escape`
   - Create prompt variants

## Expected Timeline on A100

- Complete dataset generation: 30 minutes
- Multi-model testing: 2-3 hours
- Full evaluation pipeline: 1 day

## Contact for Issues

Check logs in:
- `completions_generation.log`
- `validation_output.txt`
- `*.out` files

---

Good luck with the GPU acceleration! The A100 should make quick work of the remaining tasks.