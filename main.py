from absl import flags
import sys
from functions import (
    generate_excel_files,
    generate_partitioned_jsonl,
    generate_combined_translations,
)


FLAGS = flags.FLAGS

flags.DEFINE_enum(
    "function",
    "generate_excel_files",
    [
        "generate_excel_files",
        "generate_partitioned_jsonl",
        "generate_combined_translations",
    ],
    "Function to run.",
)


def main():
    data_folder = (
        "C:/Users/DELL/PycharmProjects/amazon_massive/data"  # Path to the data folder
    )
    # Output folder for excel files
    output_folder = "C:/Users/DELL/PycharmProjects/amazon_massive/output/excel_files"

    # Output folder for partitioned en, sw and dn
    output_folder_1 = (
        "C:/Users/DELL/PycharmProjects/amazon_massive/output/partitioned_jsonl"
    )

    # Combined translations input
    input_folder = (
        "C:/Users/DELL/PycharmProjects/amazon_massive/output/partitioned_jsonl"
    )

    # Combined translations output
    output_file = "combined_translations.json"

    if FLAGS.function == "generate_excel_files":
        generate_excel_files(data_folder, output_folder)
    elif FLAGS.function == "generate_partitioned_jsonl":
        generate_partitioned_jsonl(data_folder, output_folder_1)
    elif FLAGS.function == "generate_combined_translations":
        generate_combined_translations(input_folder, output_file)


if __name__ == "__main__":
    flags.mark_flag_as_required("function")
    FLAGS(sys.argv)
    main()
