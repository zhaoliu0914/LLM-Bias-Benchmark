import json


def generate_dataset(category: str) -> None:
    ambiguous_dataset = open(f"data/{category.lower()}_ambiguous_short_answer.jsonl", "w")
    disambiguated_dataset = open(f"data/{category.lower()}_disambiguated_short_answer.jsonl", "w")

    ambiguous_count = 0
    disambiguated_count = 0

    with open(f"templates/{category}.jsonl") as file:
        for row in file:
            content = json.loads(row)
            context_condition = content["context_condition"]
            if context_condition == "ambig":
                ambiguous_count = ambiguous_count + 1
                dataset = ambiguous_dataset
                custom_id = f"{category.lower()}-ambiguous-{ambiguous_count}"

            elif context_condition == "disambig":
                disambiguated_count = disambiguated_count + 1
                dataset = disambiguated_dataset
                custom_id = f"{category.lower()}-disambiguated-{disambiguated_count}"

            str1 = f'{{"custom_id": "{custom_id}", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "gpt-3.5-turbo-0125", "messages": [{{"role": "system", "content": "'
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
        "Religion",
        "Nationality",
        "Sexual_orientation",
    ]

    for category in categories:
        generate_dataset(category)
