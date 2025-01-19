import re
import csv
import json
import random
import pathlib
import pandas as pd

templates_folder = "templates"
dataset_folder = "data"
metadata_folder = "metadata"
result_folder = "results"
evaluation_folder = "evaluation"
debiasing_folder = "debiasing"


def generate_dataset(category: str, input_metadata: pd.DataFrame) -> None:
    # model = "gpt3-5"
    model = "gpt4o"
    ambiguous_dataset = open(f"{dataset_folder}/{category.lower()}_ambiguous_multiple_choice_{model}.jsonl", "w")
    ambiguous_dataset_metadata = open(f"{metadata_folder}/{category.lower()}_ambiguous_multiple_choice_{model}_metadata.jsonl", "w")
    disambiguated_dataset = open(f"{dataset_folder}/{category.lower()}_disambiguated_multiple_choice_{model}.jsonl", "w")
    disambiguated_dataset_metadata = open(f"{metadata_folder}/{category.lower()}_disambiguated_multiple_choice_{model}_metadata.jsonl", "w")

    ambiguous_count = 0
    disambiguated_count = 0

    with open(f"{templates_folder}/{category}.jsonl") as file:
        for row in file:
            content = json.loads(row)
            context_condition = content["context_condition"]
            question_index = content["question_index"]
            example_id = content["example_id"]
            question_polarity = content["question_polarity"]
            answer_info = content["answer_info"]
            label = content["label"]

            answer_info_str = json.dumps(answer_info)
            metadata_info = input_metadata[(input_metadata["category"] == category) & (input_metadata["question_index"] == int(question_index)) & (input_metadata["example_id"] == int(example_id))]
            # print(f"category = {category}, question_index = {question_index}, example_id = {example_id}")
            if pd.isnull(metadata_info["target_loc"].values[0]):
                target_bias = -1
            else:
                target_bias = int(metadata_info["target_loc"].values[0])

            if context_condition == "ambig":
                ambiguous_count = ambiguous_count + 1
                dataset = ambiguous_dataset
                metadata = ambiguous_dataset_metadata
                custom_id = f"{category.lower()}-ambiguous-{ambiguous_count}"

            elif context_condition == "disambig":
                disambiguated_count = disambiguated_count + 1
                dataset = disambiguated_dataset
                metadata = disambiguated_dataset_metadata
                custom_id = f"{category.lower()}-disambiguated-{disambiguated_count}"

            str1 = f'{{"custom_id": "{custom_id}", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "gpt-4o", "messages": [{{"role": "system", "content": "Answer the multiple choice question with a single number."}}, {{"role": "user", "content": "'
            str2 = '"}], "max_tokens": 1000}}'

            metadata_str = f'{{"custom_id": "{custom_id}", "question_polarity": "{question_polarity}", "answer_info": {answer_info_str}, "label": {label}, "target_bias": {target_bias}}}'

            context = content["context"]
            question = content["question"]

            options = ""
            for answer_index in range(3):
                options = options + f"({answer_index}) " + answer_info[f"ans{answer_index}"][0] + " "

            dataset.write(str1)
            dataset.write(context + " \\n ")
            dataset.write(question + " \\n ")
            dataset.write(options)
            dataset.write(str2)
            dataset.write("\n")

            metadata.write(metadata_str)
            metadata.write("\n")

    print(f"{category.lower()}_ambiguous_multiple_choice_{model}.jsonl generated {ambiguous_count} records.")
    print(f"{category.lower()}_disambiguated_multiple_choice_{model}.jsonl generated {disambiguated_count} records.")

    ambiguous_dataset.close()
    ambiguous_dataset_metadata.close()
    disambiguated_dataset.close()
    disambiguated_dataset_metadata.close()
    

if __name__ == '__main__':
    categories = [
        "Disability_status",
        "Age",
        "Physical_appearance",
        "SES",
        "Gender_identity",
        "Race_ethnicity",
        "Race_x_gender",
        "Race_x_SES",
        "Religion",
        "Nationality",
        "Sexual_orientation",
    ]

    pathlib.Path(dataset_folder).mkdir(parents=True, exist_ok=True)
    pathlib.Path(metadata_folder).mkdir(parents=True, exist_ok=True)
    pathlib.Path(evaluation_folder).mkdir(parents=True, exist_ok=True)

    input_metadata = pd.read_csv(f"{templates_folder}/additional_metadata.csv")

    for category in categories:
        generate_dataset(category, input_metadata)
