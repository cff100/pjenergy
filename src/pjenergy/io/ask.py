from pjenergy.io.console import print_combination_limit_warning
from pjenergy.config.constants import RequestFlowConstants

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


def ask_request_limit(limit) -> int:
    if limit == RequestFlowConstants.DEFAULT_REQUEST_LIMIT:
        return limit
    else:
        return ask_value("What limit do you want for each request?")


def ask_alternative_combination_limit(limit: int) -> int:

    while True:
        print_combination_limit_warning(limit) 
            
        if is_answer_yes(f"Do you want to keep this value ({limit} combinations)?"):
            break
        
        limit = ask_value("What value do you want?") 

    return limit