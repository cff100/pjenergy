

def is_answer_yes_or_no(answer: str) -> bool:
    answer = answer.strip().upper()
    return answer in ["Y", "N"]


def is_answer_yes(question: str) -> bool:
    while True:
        answer = input(question)
        if is_answer_yes_or_no(answer):
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


def ask_alternative_combination_request_limit(limit: int) -> int:

    while True:
        if limit >= 6000:
            print(f"{limit} combinations is a very costly request. \
                The request will not be prioritized and even risks not being accepted by the CDS. \
                A lower value is better.")
        else:
            print(f"{limit} combinations is a request of considerable size, \
                so it will not be prioritized by the CDS. 600 is better value")
            
        if is_answer_yes(f"Do you want to keep this value ({limit} combinations)?"):
            break
        
        
        limit = ask_value("What value do you want?") # type: ignore

    return limit