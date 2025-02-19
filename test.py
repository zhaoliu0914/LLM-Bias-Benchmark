import os
import csv
import json
import random


def validation_jsonl():
    folder = "results"
    filename_list = os.listdir(folder)
    print(f"The number of files = {len(filename_list)}")
    count = 0
    for filename in filename_list:
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and "chat_completions" in file_path:
            with open(file_path) as evaluation_file:
                # print(f"validate file = {file_path}")
                index = 0
                for evaluation_row in evaluation_file:
                    # print(f"index = {index}")
                    response = json.loads(evaluation_row)
                    # print(json.dumps(response["body"]["messages"]))
                    index += 1
                    count += 1
                # if index != 7980:
                #     print(f"The size = {index}, file = {file_path} is wrong.")

    print(f"The total records = {count}")


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
        write = csv.writer(csv_file, dialect="unix")
        write.writerow(["age", "gender"])
        write.writerow(["1", "m"])
        write.writerow(["2", "f"])

if __name__ == '__main__':
    csv_example()

    # print("==========================================")
    # filename_list = os.listdir("debiasing")
    # result_list = []
    # count = 0
    # print(f"The number of files in debiasing path = {len(filename_list)}")
    # for filename in filename_list:
    #     file_path = os.path.join("debiasing", filename)
    #     if os.path.isfile(file_path) and "DS_Store" not in file_path and "self-consistency" in file_path:
    #         count = count + 1
    #         print(file_path)
    # print(f"count = {count}")
    #
    # count = 0
    # with open("mapping files/dataset.csv") as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     header = next(csv_reader)
    #     for row in csv_reader:
    #         dataset_file_path = row[0]
    #         batch_id = row[1]
    #
    #         if "self-consistency" not in dataset_file_path:
    #             continue
    #         if "multiple_choice" in dataset_file_path:
    #             continue
    #         count = count + 1
    #         print(dataset_file_path)
    # print(f"count = {count}")

    # with open(f"batch_OmPhzphbrOEp9LStuWBy8Hes_output.jsonl") as batch_file:
    #    for row in batch_file:
    #        content = json.loads(row)
    #        print(content["response"]["body"]["choices"][0]["message"]["content"])

    # count = 0
    # total_tokens = 0
    # with open(f"results/batch_DrRndrSFnJsweyRswyFs9Eyu.jsonl") as evaluation_file:
    #    for row in evaluation_file:
    #        count = count + 1
    #        content = json.loads(row)
    #        total_tokens = total_tokens + content["response"]["body"]["usage"]["total_tokens"]
    # print(f"total_tokens = {total_tokens}")
    # print(f"count = {count}")
    # print(f"average = {total_tokens/count}")

    # with open("mapping files/dataset.csv") as csv_file:
    #    csv_reader = csv.reader(csv_file)
    #    header = next(csv_reader)
    #    for row in csv_reader:
    #        dataset_filename = row[0]
    #        batch_id = row[1]
    #        if "gpt4o" in dataset_filename:
    #            print(f"dataset_filename = {dataset_filename}")

    # content = dict()
    # message = dict()
    # choices = dict()
    # body = dict()
    # response = dict()
    # content["content"] = "This is a GPT response."
    # message["message"] = content
    # choices["choices"] = [message]
    # body["body"] = choices
    # response["response"] = body
    # str = json.dumps(response)
    # print(str)

    # debiasing_folder = "debiasing"
    # filename_list = os.listdir(debiasing_folder)
    # print(f"The number of files in path {debiasing_folder} = {len(filename_list)}")
    # for filename in filename_list:
    #    file_path = os.path.join(debiasing_folder, filename)
    #    if os.path.isfile(file_path):
    #        dataset_filename = file_path.split("/")[1]
    #        dataset_name = dataset_filename.split(".")[0]
    #        print(f"Processing debiasing file {dataset_name}")

    #        response_filename = f"chat_completions_{dataset_name}.jsonl"

    #        with open(file_path) as debiasing_file:
    #            line_count = sum(1 for line in debiasing_file)
    #            debiasing_file.seek(0)
    #            test_list = []
    #            while len(test_list) < 100:
    #                index = random.randint(1, line_count)
    #                if index not in test_list:
    #                    test_list.append(index)
    #            print(f"Number of records = {line_count}")

    #            print(test_list)

    #            for debiasing_row in debiasing_file:
    #                debiasing_content = json.loads(debiasing_row)
    #                custom_id = debiasing_content["custom_id"]
    #                #print(custom_id)
    #                tokens = custom_id.split("-")
    #                custom_id_index = tokens[len(tokens) - 1]
    #                print(f"custom_id_index = {custom_id_index}")

    # filename = "debiasing/sexual_orientation_ambiguous_multiple_choice_gpt3-5_self-debiasing.jsonl"
    # tokens = filename.split(".")[0].split("/")
    # dataset_filename = tokens[len(tokens) - 1]
    # underline_last_index = dataset_filename.rindex("_")
    # print(dataset_filename[0:underline_last_index])

    # question_type = "_fill_blank_"
    # input_filename = "data/race_x_ses_ambiguous_fill_blank_gpt4o.jsonl"
    # tokens = input_filename.split(".")[0].split("/")
    # dataset_filename = tokens[len(tokens) - 1]
    # print(dataset_filename.split(question_type)[0])

    # filename = "debiasing/gender_identity_ambiguous_multiple_choice_gpt3-5_new-debiasing.jsonl"
    # if "new-debiasing" not in filename:
    #    print("new-debiasing not in filename")
    # else:
    #    print("new-debiasing in filename")
