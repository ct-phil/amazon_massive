import os
import json
import argparse
import openpyxl
import glob
import random


def generate_excel_files(data_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

        # Iterate through each JSONL file in the data folder
    for file_name in os.listdir(data_folder):
        if file_name.endswith(".jsonl"):
            language_id = os.path.splitext(file_name)[0]

            # Read the JSONL file for the current language
            file_path = os.path.join(data_folder, file_name)
            with open(file_path, "r", encoding="utf-8") as json_file:
                lines = json_file.readlines()

            # Parse each line (record) and extract the required fields
            records = [json.loads(line.strip()) for line in lines]
            data = [
                {
                    "id": record["id"],
                    "utt": record["utt"],
                    "annot_utt": record["annot_utt"],
                }
                for record in records
            ]

            # Create a new workbook
            workbook = openpyxl.Workbook()

            # Create a new worksheet
            worksheet = workbook.active

            # Write headers
            worksheet.append(["id", "utt", "annot_utt"])

            # Write the data to the worksheet
            for record in data:
                worksheet.append([record["id"], record["utt"], record["annot_utt"]])

            # Save the workbook
            excel_filename = os.path.join(output_folder, f"en-{language_id}.xlsx")
            workbook.save(excel_filename)


def generate_partitioned_jsonl(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Languages and partitions to process
    languages = ["sw-KE", "de-DE", "en-US"]
    partitions = ["test", "train", "dev"]

    for lang in languages:
        for partition in partitions:
            input_file = os.path.join(input_folder, f"{lang}.jsonl")

            # Check if the file exists and process the partition
            if os.path.exists(input_file):
                output_file = os.path.join(output_folder, f"{lang}_{partition}.jsonl")
                data = []

                # Read the JSONL data from the input file and filter by partition
                with open(input_file, "r", encoding="utf-8") as jsonl_file:
                    for line in jsonl_file:
                        record = json.loads(line.strip())
                        if record.get("partition") == partition:
                            data.append(record)

                # Write data to the new JSONL file
                with open(output_file, "w", encoding="utf-8") as jsonl_file:
                    for record in data:
                        jsonl_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def generate_combined_translations(input_folder, output_file):
    translations = {}

    # Languages for which we want to generate translations
    languages = ["sw-KE", "de-DE", "en-US"]  # Add more languages as needed

    for lang in languages:
        train_file_path = os.path.join(input_folder, f"{lang}_train.jsonl")

        if os.path.exists(train_file_path):
            with open(train_file_path, "r", encoding="utf-8") as train_file:
                for line in train_file:
                    data = json.loads(line.strip())
                    translation_id = data["id"]
                    translation_utt = data["utt"]

                    # Add translation to the dictionary
                    translations.setdefault(lang, []).append(
                        {"id": translation_id, "utt": translation_utt}
                    )

    # Write the combined translations to a JSON file
    with open(output_file, "w", encoding="utf-8") as output_json:
        json.dump(translations, output_json, indent=4, ensure_ascii=False)
