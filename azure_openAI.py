import os
import csv
import json
from time import sleep
from datetime import datetime
from openai import OpenAI
from openai import AzureOpenAI


def load_environment_variables():
    with open("project.env") as file:
        for row in file:
            row = row.replace(" ", "")
            if not row.startswith("#"):
                position = row.index("=")
                key = row[0: position]
                value = row[position + 1: len(row)]
                os.environ[key] = value


def chat_complete():
    endpoint = "https://llm-bias-project.openai.azure.com/openai/v1/"
    deployment_name = "gpt-4o"
    api_key = os.environ["azure_openai_key"]

    client = OpenAI(
        base_url=endpoint,
        api_key=api_key
    )

    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "user",
                "content": "What is the capital of China?",
            }
        ],
    )

    print(completion.choices[0].message)


def submit_batch_job(client: AzureOpenAI, input_file: str) -> str:
    # Upload a file with a purpose of "batch"
    file = client.files.create(
        file=open(input_file, "rb"),
        purpose="batch",
        extra_body={"expires_after": {"seconds": 1209600, "anchor": "created_at"}}
        # Optional you can set to a number between 1209600-2592000. This is equivalent to 14-30 days
    )

    print(f"File expiration: {datetime.fromtimestamp(file.expires_at) if file.expires_at is not None else 'Not set'}")

    file_id = file.id
    batch_response = client.batches.create(
        input_file_id=file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        extra_body={"output_expires_after": {"seconds": 1209600, "anchor": "created_at"}}
        # Optional you can set to a number between 1209600-2592000. This is equivalent to 14-30 days
    )
    # print(batch_response.model_dump_json(indent=2))

    # Save batch ID for later use
    batch_id = batch_response.id
    print(f"batch_id = {batch_id}")
    return batch_id


def submit_datasets(client: AzureOpenAI) -> None:
    # setup for input folder
    #folder = "data"
    folder = "debiasing"
    #folder = "filler_items"
    # setup for recording .csv file
    with open("mapping files/dataset.csv", mode="a") as csv_file:
        csv_writer = csv.writer(csv_file, lineterminator="\n")
        count = 0
        filename_list = os.listdir(folder)
        for filename in filename_list:
            if "gpt-o3mini" in filename:
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    print(f"Submit {file_path} to Azure OpenAI")
                    count += 1
                    batch_job_id = submit_batch_job(client, file_path)
                    csv_writer.writerow([file_path, batch_job_id])

                    if count % 10 == 0:
                        sleep(600)

    print(f"Submitted {count} files from {folder} to OpenAI API.")


def submit_evaluation(client: AzureOpenAI) -> None:
    # setup for input folder
    folder = "evaluation"
    # setup for recording .csv file
    with open("mapping files/evaluation.csv", mode="a") as csv_file:
        csv_writer = csv.writer(csv_file, lineterminator="\n")
        count = 0
        filename_list = os.listdir(folder)
        for filename in filename_list:
            if "gpt-o3mini" in filename:
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    print(f"Submit {file_path} to Azure OpenAI")
                    count += 1
                    batch_job_id = submit_batch_job(client, file_path)
                    csv_writer.writerow([file_path, batch_job_id])

                    if count % 10 == 0:
                        sleep(500)

    print(f"Submitted {count} files from {folder} to OpenAI API.")


def retrieve_batch_job_results(client: AzureOpenAI):
    #with open("mapping files/dataset.csv", mode="r") as csv_file:
    with open("mapping files/evaluation.csv", mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        for row in csv_reader:
            dataset_filename = row[0]
            batch_id = row[1]

            if "gpt-o3mini" in dataset_filename:
                batch_response = client.batches.retrieve(batch_id)
                status = batch_response.status
                output_file_id = batch_response.output_file_id
                error_file_id = batch_response.error_file_id

                if output_file_id is not None:
                    file_response = client.files.content(output_file_id)
                    print(f"Write the result of Batch id = {batch_id} to output file = {batch_id}.jsonl")
                    with open(f"results/{batch_id}.jsonl", mode="w") as batch_file:
                        batch_file.write(file_response.text)

                if error_file_id is not None:
                    print(f"There are errors occurring in batch input file = {row[0]}, and batch id = {batch_id}")



if __name__ == '__main__':
    load_environment_variables()

    client = AzureOpenAI(
        api_key=os.environ["azure_openai_key"],
        # os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2025-03-01-preview",
        azure_endpoint="https://llm-bias-project.openai.azure.com/"  # os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    #submit_datasets(client)

    #submit_evaluation(client)

    retrieve_batch_job_results(client)

