#!/bin/bash

# Check if script name is passed
if [ $# -lt 1 ]; then
  echo "Usage: $0 <python_script>"
  exit 1
fi

PYTHON_SCRIPT="$1"
SCRIPT_NAME=$(basename "$PYTHON_SCRIPT" .py)
OUTPUT_CSV="results_${SCRIPT_NAME}.csv"

# Parameter options
workloads=("read" "write" "mixed")
num_ops=("1000")
data_sizes=("10" "100" "500" "1000" "5000" "15000" "50000" "100000")

# Write CSV header
echo "script,workload,num_ops,data_size,time_seconds" > "$OUTPUT_CSV"

# Run all combinations
for workload in "${workloads[@]}"; do
  for ops in "${num_ops[@]}"; do
    for size in "${data_sizes[@]}"; do
      echo "Running: python3 $PYTHON_SCRIPT --workload $workload --num_ops $ops --data_size $size"
      output=$(python3 "$PYTHON_SCRIPT" --workload "$workload" --num_ops "$ops" --data_size "$size")

      # Extract time using regex
      time=$(echo "$output" | grep -oE 'in [0-9.]+ seconds' | grep -oE '[0-9.]+' || echo "N/A")

      # Write to CSV
      echo "$SCRIPT_NAME,$workload,$ops,$size,$time" >> "$OUTPUT_CSV"
      sleep 3
    done
  done
done

echo "Benchmarking complete. Results saved to $OUTPUT_CSV"
