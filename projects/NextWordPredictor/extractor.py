from pathlib import Path
DATASET_DIR=Path("/mnt/d/DL-Algorithm/py150_files")
OUTPUT_FILE=Path("/mnt/d/DL-Algorithm/projects/NextWordPredictor/output.txt")
count=0
with open(OUTPUT_FILE,'w',encoding='utf8') as output:
    for file_path in DATASET_DIR.rglob("*.py"):
        try:
            code=file_path.read_text(encoding='utf-8')
            output.write(code)
            output.write("\n\n<EOS>\n\n") 
            count+1
        except Exception as e:
            print(f"Skipping{file_path}:{e}")
            