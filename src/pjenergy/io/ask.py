

def is_answer_valid(answer: str) -> bool:
    answer = answer.strip().upper()
    return answer in ["Y", "N"]


def is_answer_yes(question: str) -> bool:
    while True:
        answer = input(question)
        if is_answer_valid(answer):
            break
    return answer == "Y"

def ask_value(question: str) -> int:
    str_value = input(question)
    
    while True:
        try:
            return int(str_value)
        except TypeError:
            print("This value is not an integer.")
            str_value = input(question)