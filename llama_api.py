import json
from openai import OpenAI
from datetime import datetime


if __name__ == '__main__':
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="vllm-Llama")

    print(f"Start time = {datetime.now()}")

    dataset_name = "age_disambiguated_short_answer_llama3_cot-debiasing"
    response_filename = f"chat_completions_{dataset_name}"
    with open(f"results/{response_filename}.jsonl", "w") as debiasing_result_file:
        with open("debiasing/age_disambiguated_short_answer_llama3_cot-debiasing.jsonl") as debiasing_file:
            for debiasing_row in debiasing_file:
                debiasing_content = json.loads(debiasing_row)
                custom_id = debiasing_content["custom_id"]
                messages_str = debiasing_content["body"]["messages"]
                model = debiasing_content["body"]["model"]

                print(f"running record: custom_id = {custom_id}")

                completion = client.chat.completions.create(
                    model=model,
                    messages=messages_str,
                )
                chat_model = completion.model
                response_str = completion.choices[0].message.content
                # print(f"response_str = {response_str}")

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
                # print(f"response_json_str = {response_json_str}")
                debiasing_result_file.write(response_json_str + "\n")

    print(f"End time = {datetime.now()}")
