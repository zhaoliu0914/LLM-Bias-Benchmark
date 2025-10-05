import os
import csv
import json
import random
import concurrent.futures
from time import sleep

from openai import OpenAI
from datetime import datetime

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")


def submit_datasets() -> None:
    # setup for input folder
    folder = "data"
    # setup for recording .csv file
    with open("mapping files/dataset.csv", mode="a") as csv_file:
        csv_writer = csv.writer(csv_file, lineterminator="\n")
        #csv_writer.writerow(["dataset file", "batch job id"])

        filename_list = os.listdir(folder)
        print(f"The number of files = {len(filename_list)}")
        for filename in filename_list:
            if "llama3-1" in filename:
                dataset_name = filename.split(".")[0]
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    print(f"process dataset: {file_path}")

                    response_filename = f"chat_completions_{dataset_name}"
                    print(f"response_filename = {response_filename}")
                    with open(f"results/{response_filename}.jsonl", "w") as result_file:
                        with open(file_path) as dataset_file:
                            for dataset_row in dataset_file:
                                content = json.loads(dataset_row)
                                custom_id = content["custom_id"]
                                model = content["body"]["model"]
                                messages_str = content["body"]["messages"]

                                completion = client.chat.completions.create(
                                    model=model,
                                    messages=messages_str,
                                )
                                chat_model = completion.model
                                response_str = completion.choices[0].message.content

                                content = dict()
                                message = dict()
                                choices = dict()
                                body = dict()
                                response = dict()
                                content["content"] = response_str
                                message["message"] = content
                                choices["model"] = chat_model
                                choices["choices"] = [message]
                                body["body"] = choices
                                response["custom_id"] = custom_id
                                response["response"] = body
                                response_json_str = json.dumps(response)
                                result_file.write(response_json_str + "\n")

                    csv_writer.writerow([file_path, response_filename])


if __name__ == '__main__':
    submit_datasets()
