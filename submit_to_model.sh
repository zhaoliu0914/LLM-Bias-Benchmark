#!/bin/bash

csv_file="mapping files/dataset.csv"
# list all files from data folder.
for file in data/*; do
    if [[ $file == *"llama"* && $file == *"fill_blank"* ]]; then
        echo "Processing $file"
        filename=$(echo "$file" | cut -d "/" -f 2)
        filename=$(echo "$filename" | cut -d "." -f 1)
        result_filename="${filename}_dataset_result"
        python -m vllm.entrypoints.openai.run_batch -i "$file" -o "results/${result_filename}.jsonl" --model meta-llama/Llama-3.1-8B-Instruct --tensor-parallel-size 2
        echo "$file,$result_filename" >> "$csv_file"
    fi
done

