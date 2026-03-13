import os
import re
import csv
import json
import random
import pandas as pd

from unicodedata import category


def validation_jsonl():
    folder = "evaluation"
    filename_list = os.listdir(folder)
    print(f"The number of files = {len(filename_list)}")
    count = 0
    for filename in filename_list:
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path) as evaluation_file:
                print(f"validate file = {file_path}")
                index = 0
                for evaluation_row in evaluation_file:
                    # print(f"index = {index}")
                    #print(repr(evaluation_row[0:2758]))
                    response = json.loads(evaluation_row)
                    #print(json.dumps(response["custom_id"]))
                    index += 1
                    count += 1
                # if index != 7980:
                #     print(f"The size = {index}, file = {file_path} is wrong.")

    print(f"The total records = {count}")


def validata_debiasing_batch():
    with open("mapping files/evaluation.csv", mode="r") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        count = 0
        for line in csv_reader:
            evaluation_file = line[0]
            result_file = line[1]
            #print(f"evaluation_file = {evaluation_file}")
            #file_path = os.path.join(os.getcwd(), "results", f"{result_file}.jsonl")
            is_existing = os.path.exists(f"results/{result_file}.jsonl")
            if is_existing:
                with open(f"results/{result_file}.jsonl") as evaluation_result_file:
                    for row in evaluation_result_file:
                        response = json.loads(row)
            else:
                count += 1
                print(f"The results of {evaluation_file} does not exist.")
        print(f"count = {count}")


def correct_multiple_choice_answer():
    folder = "results"
    filename_list = os.listdir(folder)
    #count = 0
    for filename in filename_list:
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and "cot-debiasing" in filename and "multiple_choice" in filename and "ambiguous" in filename:
            #print(file_path)
            category = filename.split("chat_completions_")[1].split("_multiple_choice")[0]
            #print(category)
            metadata_list = []
            with open(f"metadata/{category}_metadata.jsonl") as metadata_file:
                for row in metadata_file:
                    content = json.loads(row)
                    metadata_list.append(content)
            rewrite_answer_list = []
            with open(file_path) as multiple_choice_file:
                for multiple_choice_row in multiple_choice_file:
                    response = json.loads(multiple_choice_row)
                    custom_id = response["custom_id"]
                    answer = response["response"]["body"]["choices"][0]["message"]["content"]
                    answer = answer.lower()

                    for metadata in metadata_list:
                        metadata_custom_id = metadata["custom_id"]
                        if metadata_custom_id == custom_id:
                            #correct_answer = str(metadata["label"])
                            if metadata["answer_info"]["ans0"][1] == "unknown":
                                unknown_answer = "0"
                            elif metadata["answer_info"]["ans1"][1] == "unknown":
                                unknown_answer = "1"
                            else:
                                unknown_answer = "2"
                            break
                    # print(custom_id)
                    # print(answer)
                    # print(correct_answer)
                    if "cannot" in answer or "unknown" in answer or "ambiguous" in answer:
                        response["response"]["body"]["choices"][0]["message"]["content"] = unknown_answer

                    rewrite_answer_list.append(json.dumps(response))

            #new_filename = filename.split(".jsonl")[0] + "_new"
            #rewrite_file_path = os.path.join(folder, new_filename+".jsonl")
            print(f"re-write file = {file_path}")
            with open(file_path, mode="w") as rewrite_file:
               for new_answer in rewrite_answer_list:
                   rewrite_file.write(new_answer + "\n")


def remove_files_based_on_debiasing():
    file_pattern = "cot-debiasing"

    count = 0
    # Remove debiasing files
    folder = "debiasing"
    filename_list = os.listdir(folder)
    for filename in filename_list:
        file_path = os.path.join(folder, filename)
        if file_pattern in filename:
            os.remove(file_path)
            count += 1
    print(f"Removed {count} files from debiasing folder")

    count = 0
    # Remove chat_completions files
    folder = "results"
    filename_list = os.listdir(folder)
    for filename in filename_list:
        file_path = os.path.join(folder, filename)
        if file_pattern in filename:
            os.remove(file_path)
            count += 1
    print(f"Removed {count} chat_completions files from results folder")

    remove_list = []
    df = pd.read_csv("mapping files/dataset.csv")
    dataset_file = df["dataset file"]
    for index, dataset in enumerate(dataset_file):
        if file_pattern in dataset:
            remove_list.append(index)
    df = df.drop(remove_list)
    df.to_csv("mapping files/dataset.csv", index=False)
    print(f"Removed {len(remove_list)} rows from mapping files/dataset.csv")

    count = 0
    remove_list = []
    df = pd.read_csv("mapping files/evaluation.csv")
    evaluation_files = df["evaluation file"]
    batch_job_ids = df["batch job id"]
    for index, evaluation_file in enumerate(evaluation_files):
        if file_pattern in evaluation_file:
            remove_list.append(index)
            file_path = os.path.join("results", f"{batch_job_ids[index]}.jsonl")
            os.remove(file_path)
            os.remove(evaluation_file)
            count += 1
    df = df.drop(remove_list)
    df.to_csv("mapping files/evaluation.csv", index=False)
    print(f"Removed {count} files from evaluation folder")
    print(f"Removed {count} files from results folder")
    print(f"Removed {len(remove_list)} rows from mapping files/evaluation.csv")


def os_path_example():
    separator = os.path.sep
    print(f"separator = {separator}")

    file_path = "data/age_ambiguous_fill_blank_gpt3-5.jsonl"
    with open(file_path) as file:
        for line in file:
            json.loads(line)
            print(f"line = {line}")


def csv_example():
    with open("test.csv", mode="a") as csv_file:
        write = csv.writer(csv_file, lineterminator="\n")
        write.writerow(["age", "gender"])
        write.writerow(["1", "m"])
        write.writerow(["2", "f"])


def read_file_line_terminator():
    line_list = []
    with open("test.txt", mode="r") as file:
        for line in file:
            line_list.append(line.strip())

    print(line_list)


def rename_files_under_folder():
    files = os.listdir("filler_items")
    for file in files:
        print(file)

        tokens = file.split("gpt4o_filler_items")
        prefix = tokens[0]
        postfix = tokens[1]

        print(f"prefix = {prefix}")
        print(f"postfix = {postfix}")

        print(f"new file name = filler_items/{prefix}filler_items_gpt4o{postfix}")

        os.rename(f"filler_items/{file}", f"filler_items/{prefix}filler_items_gpt4o{postfix}")


def generate_filler_items():
    #model = "gpt-4o"
    model = "gpt-o3mini"
    #model = "meta-llama/Llama-3.1-8B-Instruct"
    #model = "google/gemma-3-27b-it"


    files = os.listdir("filler_items")
    for file in files:
        if "gpt4o" in file:

            # It's only required for initial generation
            # count = 0
            # with open(f"data/{file}") as json_file:
            #     for row in json_file:
            #         count += 1
            # id_set = set()
            # while len(id_set) < 72:
            #     temp_i = random.randint(1, count)
            #     id_set.add(str(temp_i))
            # print(id_set)

            dataset_name = file.split(".")[0]
            print(f"Processing dataset: {dataset_name}")

            with open(f"filler_items/{file}") as json_file:
                with open(f"filler_items/{file.replace('gpt4o', 'gpt-o3mini')}", "w") as dataset_file:

                    for row in json_file:
                        content = json.loads(row)

                        # It's only required for initial generation
                        # custom_id = content["custom_id"]
                        # temp_tokens = custom_id.split("-")
                        # temp_id = temp_tokens[len(temp_tokens) - 1]
                        # if temp_id not in id_set:
                        #     continue

                        content["body"]["model"] = model
                        del content["body"]["max_tokens"]
                        content["body"]["max_completion_tokens"] = 20000

                        content_str = json.dumps(content)
                        dataset_file.write(content_str + "\n")


def generate_assess_evaluation():
    templates_folder = "templates"
    dataset_folder = "data"
    metadata_folder = "metadata"
    result_folder = "results"
    evaluation_folder = "evaluation"

    number_total = 0
    with open(f"test.txt", "w") as marked_answer_file:

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
                #print(f"dataset_name = {dataset_name}")
                if "age" in dataset_name or "nationality" in dataset_name:
                    continue
                if "debiasing" in dataset_name or "filler_items" in dataset_name:
                    continue
                if "ambiguous" in dataset_name:
                    continue
                if "multiple_choice" in dataset_name:
                    continue
                if "gpt3-5" in dataset_name or "gpt4o" in dataset_name or "llama3-1" in dataset_name:
                    continue

                print(f"Processing dataset {dataset_name}")

                id_set = set()
                count = 0
                with open(dataset_input_file) as file:
                    for row in file:
                        count += 1
                while len(id_set) < 15:
                    temp_i = random.randint(1, count)
                    id_set.add(str(temp_i))

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

                    if "_fill_blank_" in dataset_name:
                        metadata_filename = dataset_name.split("_fill_blank_")[0]
                    elif "_short_answer_" in dataset_name:
                        metadata_filename = dataset_name.split("_short_answer_")[0]
                    metadata_list = []
                    with open(f"{metadata_folder}/{metadata_filename}_metadata.jsonl") as metadata_file:
                        for row in metadata_file:
                            content = json.loads(row)
                            metadata_list.append(content)

                    for row in dataset:
                        content = json.loads(row)
                        custom_id = content["custom_id"]

                        temp_tokens = custom_id.split("-")
                        temp_id = temp_tokens[len(temp_tokens) - 1]
                        if temp_id not in id_set:
                            continue

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
                                break

                        for evaluation in evaluation_list:
                            evaluation_custom_id = evaluation["custom_id"]
                            if evaluation_custom_id == custom_id:
                                evaluation_result = evaluation["response"]["body"]["choices"][0]["message"]["content"]
                                break

                        # if is_correct is False:
                        for response_answer in answer_list:
                            response_custom_id = response_answer["custom_id"]
                            if response_custom_id == custom_id:
                                response_answer_str = response_answer["response"]["body"]["choices"][0]["message"]["content"]
                                break
                                # response_answer_str = pattern.sub(r"\1.\n", response_answer_str)

                        marked_answer_file.write(
                            "======================================================================\n")
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
                        marked_answer_file.write("Evaluation: " + "\n")
                        marked_answer_file.write(evaluation_result + "\n")
                        marked_answer_file.write("\n")
                        marked_answer_file.write("Label:\n")
                        marked_answer_file.write(
                            "======================================================================\n")
                        marked_answer_file.write("\n")
                        marked_answer_file.write("\n")

                        number_total = number_total + 1
                        if number_total == 460:
                            print(f"Finished generate 460 Assess Evaluation records.")
                            return


if __name__ == '__main__':
    # validation_jsonl()
    # rename_files_under_folder()

    #generate_filler_items()

    generate_assess_evaluation()




