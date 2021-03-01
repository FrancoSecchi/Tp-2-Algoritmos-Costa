def user_answer_is_yes(input_user: str):
    """
    
    :param input_user:
    :return:
    """
    if input_user.isnumeric() or (input_user.lower() not in ["yes", "ye", "y"]):
        return False
    return True
