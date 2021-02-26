def user_answer_is_yes(input_user: str):
    """
    
    :param input_user:
    :return:
    """
    if input_user.isnumeric() or input_user not in ["yes", "y", "si"]:
        return False
    return True
