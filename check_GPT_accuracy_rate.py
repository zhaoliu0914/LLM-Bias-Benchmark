import re
import csv
import json
import random
import pathlib


templates_folder = "templates"
dataset_folder = "data"
metadata_folder = "metadata"
result_folder = "results"
evaluation_folder = "evaluation"


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
    ambiguous = "ambiguous"
    unknown = "unknown"
    accuracy_map = dict()
    bias_score_map = dict()

    pattern = re.compile(r"(?<![0-9])([a-zA-Z])\. ")

    with open("mapping files/dataset.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        evaluation_map = dict()
        with open("mapping files/evaluation.csv") as evaluation_csv_file:
            evaluation_csv_reader = csv.reader(evaluation_csv_file)
            evaluation_header = next(evaluation_csv_reader)
            for row in evaluation_csv_reader:
                evaluation_input_file = row[0]
                batch_id = row[1]
                evaluation_filename = evaluation_input_file.split("/")[1]
                evaluation_map[evaluation_filename] = batch_id

        for csv_row in csv_reader:
            dataset_input_file = csv_row[0]
            batch_id = csv_row[1]

            dataset_filename = dataset_input_file.split("/")[1]
            dataset_name = dataset_filename.split(".")[0]
            # "age_ambiguous_short_answer"
            # "ses_ambiguous_short_answer"
            if "ses_ambiguous_short_answer" not in dataset_name:
                continue

            print(f"Processing dataset {dataset_name}")
            marked_answer_file = open(f"marked answer/{dataset_name}.txt", "w")

            accuracy_map[dataset_name] = None
            bias_score_map[dataset_name] = None
            number_total = 0
            number_correct = 0
            number_non_unknown = 0
            number_target_bias = 0
            with open(f"{dataset_input_file}") as dataset:
                answer_list = []
                with open(f"{result_folder}/{batch_id}.jsonl") as answer_file:
                    for row in answer_file:
                        content = json.loads(row)
                        answer_list.append(content)

                evaluation_list = []
                # multiple choice does not have evaluation by Prompt Engineering, so it could read the response answer directly.
                if "multiple_choice" in dataset_input_file:
                    with open(f"{result_folder}/{batch_id}.jsonl") as evaluation_file:
                        for row in evaluation_file:
                            content = json.loads(row)
                            evaluation_list.append(content)
                else:
                    with open(f"{result_folder}/{evaluation_map[dataset_filename]}.jsonl") as evaluation_file:
                        for row in evaluation_file:
                            content = json.loads(row)
                            evaluation_list.append(content)

                metadata_list = []
                with open(f"{metadata_folder}/{dataset_name}_metadata.jsonl") as metadata_file:
                    for row in metadata_file:
                        content = json.loads(row)
                        metadata_list.append(content)

                for row in dataset:
                    number_total = number_total + 1

                    content = json.loads(row)
                    custom_id = content["custom_id"]
                    question_system = content["body"]["messages"][0]["content"]
                    question_user = content["body"]["messages"][1]["content"]
                    correct_answer = None
                    target_bias_answer = None
                    unknown_answer = None
                    response_answer_str = None
                    answer_info_str = None

                    for metadata in metadata_list:
                        metadata_custom_id = metadata["custom_id"]
                        if metadata_custom_id == custom_id:
                            correct_answer = str(metadata["label"])
                            target_bias_answer = str(metadata["target_bias"])
                            answer_info = metadata["answer_info"]
                            answer_info_str = json.dumps(answer_info)
                            #if metadata["answer_info"]["ans0"][1] == unknown:
                            #    unknown_answer = "0"
                            #elif metadata["answer_info"]["ans1"][1] == unknown:
                            #    unknown_answer = "1"
                            #else:
                            #    unknown_answer = "2"

                    is_correct = False
                    for evaluation in evaluation_list:
                        evaluation_custom_id = evaluation["custom_id"]
                        if evaluation_custom_id == custom_id:
                            evaluation_result = evaluation["response"]["body"]["choices"][0]["message"]["content"]

                            # filter correct answer for calculating accuracy
                            if correct_answer in evaluation_result:
                                #number_correct = number_correct + 1
                                is_correct = True

                            # filter non-unknown and target_bias for calculating basic bias scores
                            #if unknown_answer not in evaluation_result:
                            #    number_non_unknown = number_non_unknown + 1
                            #    if target_bias_answer in evaluation_result:
                            #        number_target_bias = number_target_bias + 1

                    if is_correct is False:
                        for response_answer in answer_list:
                            response_custom_id = response_answer["custom_id"]
                            if response_custom_id == custom_id:
                                response_answer_str = response_answer["response"]["body"]["choices"][0]["message"]["content"]
                                response_answer_str = pattern.sub(r"\1.\n", response_answer_str)

                        marked_answer_file.write("======================================================================\n")
                        marked_answer_file.write(custom_id + "\n")
                        marked_answer_file.write("Question:" + "\n")
                        marked_answer_file.write(question_system + "\n")
                        marked_answer_file.write(question_user + "\n")
                        marked_answer_file.write("\n")
                        marked_answer_file.write("Options:\n")
                        marked_answer_file.write(answer_info_str + "\n")
                        marked_answer_file.write("Correct Answer:\n")
                        marked_answer_file.write(correct_answer + "\n")
                        marked_answer_file.write("Target Bias:\n")
                        marked_answer_file.write(target_bias_answer + "\n")
                        marked_answer_file.write("Answer: " + "\n")
                        marked_answer_file.write(response_answer_str + "\n")
                        marked_answer_file.write("\n")
                        marked_answer_file.write("Label:\n")
                        marked_answer_file.write("======================================================================\n")
                        marked_answer_file.write("\n")
                        marked_answer_file.write("\n")

            marked_answer_file.close()