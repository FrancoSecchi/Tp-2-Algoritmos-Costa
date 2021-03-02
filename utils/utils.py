def user_answer_is_yes(input_user: str) -> bool:
    """
    Check if the user input is affirmative
    
    Arguments:
        input_user (str): The user input
    
    Returns:
        bool
    """
    if input_user.isnumeric() or (input_user.lower() not in ["yes", "ye", "y"]):
        return False
    return True
