import csv
import json
import random
import pathlib


def check_batch_job_accuracy():
    with open("mapping files/evaluation.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        for row in csv_reader:
            evaluation_input_file = row[0]
            batch_id = row[1]

            tokens = evaluation_input_file.split(".")[0].split("/")

            evaluation_file = open(f"evaluation results/{tokens[len(tokens)-1]}.txt", "w")

            with open(f"{evaluation_input_file}") as dataset_file:
                response_list = []
                with open(f"results/{batch_id}.jsonl") as response_file:
                    for response_row in response_file:
                        response = json.loads(response_row)
                        response_list.append(response)

                for row in dataset_file:
                    dataset_content = json.loads(row)
                    custom_id = dataset_content["custom_id"]
                    question = dataset_content["body"]["messages"][0]["content"]

                    messages = dataset_content["body"]["messages"]
                    for message_index in range(len(messages)):
                        role = messages[message_index]["role"]
                        if role == "user":
                            question = question + "\n" + messages[message_index]["content"]
                            break

                    answer = ""
                    for response in response_list:
                        response_custom_id = response["custom_id"]
                        if response_custom_id == custom_id:
                            answer = response["response"]["body"]["choices"][0]["message"]["content"]

                    evaluation_file.write("======================================================================\n")
                    evaluation_file.write(custom_id + "\n")
                    evaluation_file.write("Question:" + "\n")
                    evaluation_file.write(question + "\n")
                    evaluation_file.write("\n")
                    evaluation_file.write("Answer: " + "\n")
                    evaluation_file.write(answer + "\n")
                    evaluation_file.write("\n")
                    evaluation_file.write("Label:\n")
                    evaluation_file.write("======================================================================\n")
                    evaluation_file.write("\n")
                    evaluation_file.write("\n")

            evaluation_file.close()


def check_chat_completion_accuracy():
    print()


if __name__ == '__main__':
    check_batch_job_accuracy()