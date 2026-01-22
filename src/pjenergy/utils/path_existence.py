
def ask_replace_file() -> bool:
    while True:
        answer = input("File already exists. Replace? (Y/N): ").strip().upper() 
        if answer in ["Y", "N"]:
            break
    return answer == "Y"
