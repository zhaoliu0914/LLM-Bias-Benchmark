import json
from openai import OpenAI

if __name__ == '__main__':
    file_name_batch_list = list()
    file_name_list = list()
    batch_id_list = list()

    with open("openai.log", "r") as logfile:
        for row in logfile:
            if "FileObject(id=" in row:
                row = row[48: len(row) - 2]
                print(row)
                file_id_str = "id='"
                file_name_str = "filename='"
                end_str = "',"

                file_id_start_index = row.find(file_id_str)
                file_id_end_index = row.find(end_str, file_id_start_index, len(row))
                file_id = row[file_id_start_index + len(file_id_str): file_id_end_index]
                print(f"file_id = {file_id}")

                file_name_start_index = row.find(file_name_str)
                file_name_end_index = row.find(end_str, file_name_start_index, len(row))
                file_name = row[file_name_start_index + len(file_name_str): file_name_end_index]
                print(f"file_name = {file_name}")

                file_name_map = dict()
                file_name_map["file_id"] = file_id
                file_name_map["file_name"] = file_name

                file_name_list.append(file_name_map)

            elif "Batch(id" in row:
                row = row[31: len(row) - 2]
                print(row)
                file_id_str = "input_file_id='"
                batch_id_str = "id='"
                end_str = "',"

                file_id_start_index = row.find(file_id_str)
                file_id_end_index = row.find(end_str, file_id_start_index, len(row))
                file_id = row[file_id_start_index + len(file_id_str): file_id_end_index]
                print(f"file_id = {file_id}")

                batch_id_start_index = row.find(batch_id_str)
                batch_id_end_index = row.find(end_str, batch_id_start_index, len(row))
                batch_id = row[batch_id_start_index + len(batch_id_str): batch_id_end_index]
                print(f"batch_id = {batch_id}")

                batch_id_map = dict()
                batch_id_map["file_id"] = file_id
                batch_id_map["batch_id"] = batch_id

                batch_id_list.append(batch_id_map)

    print("==========================")

    for file_name_map in file_name_list:
        file_name_batch_map = dict()

        file_id = file_name_map['file_id']
        file_name = file_name_map['file_name']

        file_name_batch_map["file_name"] = file_name

        for batch_id_map in batch_id_list:
            if batch_id_map["file_id"] == file_id:
                file_name_batch_map["batch_id"] = batch_id_map["batch_id"]

        file_name_batch_list.append(file_name_batch_map)

    filename_batch_mapping = open(f"filename_batch_mapping.txt", "a")
    for file_name_batch_map in file_name_batch_list:
        print(f"file_name = {file_name_batch_map['file_name']}")
        print(f"batch_id = {file_name_batch_map['batch_id']}")

        filename_batch_mapping.write(f"file_name = {file_name_batch_map['file_name']}")
        filename_batch_mapping.write("\n")
        filename_batch_mapping.write(f"batch_id = {file_name_batch_map['batch_id']}")
        filename_batch_mapping.write("\n")
    filename_batch_mapping.close()