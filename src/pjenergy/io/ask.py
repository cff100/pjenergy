"""User prompt helpers for the ERA5 request flow."""

from pjenergy.io.console import print_combination_limit_warning
from pjenergy.config.constants import RequestFlowConstants

def is_answer_yes_or_no(answer: str) -> bool:
    """Return True if the answer is a valid yes/no response (Y or N)."""
    answer = answer.strip().upper()
    return answer in ["Y", "N"]


def is_answer_yes(question: str) -> bool:
    """Prompt the user until a Y/N response is given; return True if Y."""
    while True:
        answer = input(question)
        if is_answer_yes_or_no(answer):
            break
    return answer == "Y"

def ask_value(question: str) -> int:
    """Prompt the user for an integer value, retrying until valid."""
    str_value = input(question)
    
    while True:
        try:
            return int(str_value)
        except TypeError:
            print("This value is not an integer.")
            str_value = input(question)


def ask_alternative_combination_limit(limit: int) -> int:
    """
    Ask the user to keep or change a parameter combination limit.

    :param limit: Current combination limit.
    :type limit: int
    :return: The chosen limit.
    :rtype: int
    """

    while True:
        print_combination_limit_warning(limit) 
            
        if is_answer_yes(f"Do you want to keep this value ({limit} combinations) (Y/N)?"):
            break
        
        limit = ask_value("What value do you want?") 

    return limit
