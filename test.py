import os
import csv
import json

if __name__ == '__main__':

    folder = "evaluation"
    filename_list = os.listdir(folder)
    print(f"The number of files = {len(filename_list)}")
    for filename in filename_list:
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path) as evaluation_file:
                print(f"validate file = {file_path}")
                index = 1
                for evaluation_row in evaluation_file:
                    #print(f"index = {index}")
                    response = json.loads(evaluation_row)

                    index = index + 1

                print(f"file = {file_path} is correct.")

    #with open(f"batch_OmPhzphbrOEp9LStuWBy8Hes_output.jsonl") as batch_file:
    #    for row in batch_file:
    #        content = json.loads(row)
    #        print(content["response"]["body"]["choices"][0]["message"]["content"])

    #count = 0
    #total_tokens = 0
    #with open(f"results/batch_DrRndrSFnJsweyRswyFs9Eyu.jsonl") as evaluation_file:
    #    for row in evaluation_file:
    #        count = count + 1
    #        content = json.loads(row)
    #        total_tokens = total_tokens + content["response"]["body"]["usage"]["total_tokens"]
    #print(f"total_tokens = {total_tokens}")
    #print(f"count = {count}")
    #print(f"average = {total_tokens/count}")

    #with open("mapping files/dataset.csv") as csv_file:
    #    csv_reader = csv.reader(csv_file)
    #    header = next(csv_reader)
    #    for row in csv_reader:
    #        dataset_filename = row[0]
    #        batch_id = row[1]
    #        if "gpt4o" in dataset_filename:
    #            print(f"dataset_filename = {dataset_filename}")
