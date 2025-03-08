# SecLLMHolmes Security Steering Dataset

This dataset has been prepared for security steering using examples from the [SecLLMHolmes](https://github.com/ai4cloudops/SecLLMHolmes) dataset. It contains pairs of vulnerable and secure code from both hand-crafted examples and real-world CVEs.

## Dataset Statistics

- **Total examples**: 39
- **Hand-crafted examples**: 24
- **Real-world examples**: 15

## CWE Breakdown

| CWE ID | Description | Count |
|--------|-------------|-------|
| CWE-190 | Integer Overflow | 7 |
| CWE-787 | Out-of-bounds Write | 9 |
| CWE-476 | NULL Pointer Dereference | 7 |
| CWE-416 | Use After Free | 4 |
| CWE-89 | SQL Injection | 3 |
| CWE-79 | Cross-site Scripting (XSS) | 3 |
| CWE-77 | Command Injection | 3 |
| CWE-22 | Path Traversal | 3 |

## Dataset Structure

Each example in the dataset contains:

- **prompt**: The vulnerable code snippet prefixed with "Security review of this code:"
- **completion**: The statement "This code contains security vulnerabilities."
- **mutated_program**: The secure/patched version of the code
- **source**: Either "hand-crafted" or "real-world"
- **cwe**: The CWE identifier for the vulnerability
- **vulnerability_type**: A more specific name for the vulnerability type
- **idx**: Example index
- **typechecks**: Boolean indicating if the code typechecks (always true in this dataset)

For real-world examples, additional fields may include:
- **cve**: The CVE identifier
- **project**: The source project (e.g., "gpac", "libtiff", "linux")

## Examples

### Hand-crafted Example (CWE-190: Integer Overflow)

```c
// Vulnerable code
char** initialize_data(int num_char, char* init_chars)
{
    int len_init = strlen(init_chars);
    char** data = (char**)malloc(sizeof(char*) * num_char);
    for (int i = 0; i < num_char; i++)
    {
        data[i] = (char*)malloc(sizeof(char) * len_init);
    }
    for (int i = 0; i < num_char; i++)
    {
        data[i] = init_chars;
    }
    return data;
}

// Secure code
char** initialize_data(int num_char, char* init_chars)
{
    if (num_char < 0 || num_char >= (INT_MAX / sizeof(char*)))
    {
        return NULL;
    }
    
    int len_init = strlen(init_chars);
    char** data = (char**)malloc(sizeof(char*) * num_char);
    for (int i = 0; i < num_char; i++)
    {
        data[i] = (char*)malloc(sizeof(char) * len_init);
    }
    for (int i = 0; i < num_char; i++)
    {
        data[i] = len_init;
    }
    return data;
}
```

### Real-world Example (CWE-787: Out-of-bounds Write)

From a real CVE in the gpac project (shortened for brevity).

## Usage

To use this dataset for steering:

```bash
python3 -m steering.run_steering --model bigcode/starcoderbase-1b \
--output_dir security_steering_results \
--test_split datasets/codexglue/CodeXGLUE/Code-Code/Defect-detection/dataset/test.jsonl \
--test_steer_batch_size 32 \
--test_batch_size 32 \
--steering_file ./security_steering_data.json
```

## Benefits of Using SecLLMHolmes

1. **Purpose-built for security evaluation**: The dataset was specifically created to evaluate LLMs' ability to identify and reason about security vulnerabilities.

2. **Well-structured organization**: Examples are carefully categorized by vulnerability type.

3. **Quality examples**: Hand-crafted examples clearly demonstrate specific security issues, while real-world examples come from actual CVEs in open-source projects.

4. **Balanced coverage**: Includes a variety of vulnerability types to provide comprehensive steering.

5. **Realistic scenarios**: The real-world CVEs provide authentic examples that are representative of actual vulnerabilities. 