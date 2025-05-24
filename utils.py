import os
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
        if os.path.isfile(file_path) and "cot-debiasing" in file_path:
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
        if os.path.isfile(file_path) and "cot-debiasing" in filename and "multiple_choice" in filename:
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
                    if "cannot" in answer or "Cannot" in answer:
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





if __name__ == '__main__':
    validation_jsonl()



