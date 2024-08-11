import json
import pandas as pd


def generate_dataset(category: str, additional_metadata: pd.DataFrame) -> None:
    ambiguous_dataset = open(f"data/{category.lower()}_ambiguous_short_answer.jsonl", "w")
    disambiguated_dataset = open(f"data/{category.lower()}_disambiguated_short_answer.jsonl", "w")

    ambiguous_count = 0
    disambiguated_count = 0

    with open(f"templates/{category}.jsonl") as file:
        for row in file:
            content = json.loads(row)
            context_condition = content["context_condition"]
            question_index = content["question_index"]
            example_id = content["example_id"]
            question_polarity = content["question_polarity"]
            answer_info = content["answer_info"]
            label = content["label"]
            metadata_info = additional_metadata[(additional_metadata["category"] == category) & (additional_metadata["question_index"] == int(question_index)) & (additional_metadata["example_id"] == int(example_id))]
            # print(f"category = {category}, question_index = {question_index}, example_id = {example_id}")
            if pd.isnull(metadata_info["target_loc"].values[0]):
                target_bias = -1
            else:
                target_bias = int(metadata_info["target_loc"].values[0])

            if context_condition == "ambig":
                ambiguous_count = ambiguous_count + 1
                dataset = ambiguous_dataset
                custom_id = f"{category.lower()}-ambiguous-{ambiguous_count}"

            elif context_condition == "disambig":
                disambiguated_count = disambiguated_count + 1
                dataset = disambiguated_dataset
                custom_id = f"{category.lower()}-disambiguated-{disambiguated_count}"

            str1 = f'{{"custom_id": "{custom_id}", "method": "POST", "url": "/v1/chat/completions", "question_polarity": "{question_polarity}", "answer_info": {answer_info}, "label": {label}, "target_bias": {target_bias}, "body": {{"model": "gpt-3.5-turbo-0125", "messages": [{{"role": "system", "content": "'
            str2 = '"}, {"role": "user", "content": "'
            str3 = " Could you give us the most possible answer and provide your chain of thought?"
            str4 = '"}], "max_tokens": 1000}}'

            context = content["context"]
            question = content["question"]

            dataset.write(str1)
            dataset.write(context)
            dataset.write(str2)
            dataset.write(question)
            dataset.write(str3)
            dataset.write(str4)
            dataset.write("\n")

    print(f"{category.lower()}_ambiguous_short_answer.jsonl has generated {ambiguous_count} records.")
    print(f"{category.lower()}_disambiguated_short_answer.jsonl has generated {disambiguated_count} records.")

    ambiguous_dataset.close()
    disambiguated_dataset.close()


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

    additional_metadata = pd.read_csv("templates/additional_metadata.csv")

    for category in categories:
        generate_dataset(category, additional_metadata)
