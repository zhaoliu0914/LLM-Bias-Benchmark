#!/bin/bash

model="meta-llama/Llama-3.1-8B-Instruct"
csv_file="mapping files/dataset.csv"

function submit_dataset() {
    source_folder="data/*"
    # list all files from data folder.
    for file in ${source_folder}; do
        if [[ $file == *"llama"* ]]; then
            echo "Processing $file"
            filename=$(echo "$file" | cut -d "/" -f 2)
            filename=$(echo "$filename" | cut -d "." -f 1)
            result_filename="${filename}_dataset_result"
            python -m vllm.entrypoints.openai.run_batch -i "$file" -o "results/${result_filename}.jsonl" --model ${model} --tensor-parallel-size 2
            echo "$file,$result_filename" >> "$csv_file"
        fi
    done
}


function submit_debiasing() {
    source_folder="debiasing/*"
    # list all files from data folder.
    for file in ${source_folder}; do
        if [[ $file == *"llama"* ]]; then
            echo "Processing $file"
            filename=$(echo "$file" | cut -d "/" -f 2)
            filename=$(echo "$filename" | cut -d "." -f 1)
            result_filename="${filename}_debiasing_result"
            python -m vllm.entrypoints.openai.run_batch -i "$file" -o "results/${result_filename}.jsonl" --model ${model} --tensor-parallel-size 2
            echo "$file,$result_filename" >> "$csv_file"
        fi
    done
}


submit_debiasing

