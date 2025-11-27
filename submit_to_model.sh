#!/bin/bash

number_of_gpus=2
model="google/gemma-3-27b-it"
csv_file="mapping files/dataset.csv"

function submit_dataset() {
    source_folder="data/*"
    # list all files from data folder.
    for file in ${source_folder}; do
        if [[ $file == *"gemma"* ]]; then
            echo "Processing $file"
            filename=$(echo "$file" | cut -d "/" -f 2)
            filename=$(echo "$filename" | cut -d "." -f 1)
            result_filename="${filename}_result"
            python -m vllm.entrypoints.openai.run_batch -i "$file" -o "results/${result_filename}.jsonl" --model ${model} --tensor-parallel-size ${number_of_gpus}
            echo "$file,$result_filename" >> "$csv_file"
        fi
    done
}


function submit_debiasing() {
    source_folder="debiasing/*"
    # list all files from data folder.
    for file in ${source_folder}; do
        if [[ $file == *"gemma"* ]]; then
            echo "Processing $file"
            filename=$(echo "$file" | cut -d "/" -f 2)
            filename=$(echo "$filename" | cut -d "." -f 1)
            result_filename="${filename}_result"
            python -m vllm.entrypoints.openai.run_batch -i "$file" -o "results/${result_filename}.jsonl" --model ${model} --tensor-parallel-size ${number_of_gpus}
            echo "$file,$result_filename" >> "$csv_file"
        fi
    done
}


submit_dataset

