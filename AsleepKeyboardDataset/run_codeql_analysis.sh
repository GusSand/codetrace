#!/bin/bash
# Run CodeQL analysis on AsleepKeyboardDataset scenarios with custom queries

CODEQL_PATH="../codeql-setup/codeql/codeql"
TEST_DIR="test_scenarios"
RESULTS_DIR="codeql_results"

mkdir -p "$RESULTS_DIR"

echo "Running CodeQL analysis with custom queries..."

# Read test plan
while IFS= read -r line; do
    # Parse JSON to get scenario info
    scenario_id=$(echo "$line" | jq -r '.scenario_id')
    test_file=$(echo "$line" | jq -r '.test_file')
    custom_query=$(echo "$line" | jq -r '.custom_queries[0]')
    language=$(echo "$line" | jq -r '.language')
    
    if [[ "$scenario_id" != "null" ]]; then
        echo "\nAnalyzing $scenario_id..."
        
        # Create temporary directory for this analysis
        temp_dir=$(mktemp -d)
        cp "$test_file" "$temp_dir/"
        
        # Create database based on language
        if [[ "$language" == "python" ]]; then
            db_lang="python"
        elif [[ "$language" == "c" || "$language" == "cpp" ]]; then
            db_lang="cpp"
        else
            echo "Unsupported language: $language"
            continue
        fi
        
        # Create CodeQL database
        $CODEQL_PATH database create "$temp_dir/db" \
            --language="$db_lang" \
            --source-root="$temp_dir" \
            --overwrite 2>/dev/null
        
        if [ $? -eq 0 ]; then
            # Run custom query
            output_file="$RESULTS_DIR/${scenario_id//\//_}.sarif"
            $CODEQL_PATH database analyze "$temp_dir/db" \
                "$custom_query" \
                --format=sarif-latest \
                --output="$output_file" 2>/dev/null
            
            echo "Results saved to: $output_file"
        else
            echo "Failed to create database for $scenario_id"
        fi
        
        # Cleanup
        rm -rf "$temp_dir"
    fi
done < <(jq -c '.scenarios[]' "$TEST_DIR/test_plan.json")

echo "\nAnalysis complete!"
