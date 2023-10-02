@echo off
setlocal enabledelayedexpansion

if "%1" == "generate_excel_files" (
    python main.py --function=generate_excel_files
) else if "%1" == "generate_partitioned_jsonl" (
    python main.py --function=generate_partitioned_jsonl
) else if "%1" == "generate_combined_translations" (
    python main.py --function=generate_combined_translations
) else (
    echo Unknown function: %1
)

endlocal