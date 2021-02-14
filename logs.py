from datetime import datetime
import os

GET_NAME = 0
SAVE_USER = 1


def get_formatted_time() -> str:
    """
    :return
    """
    now = datetime.now()
    hours = now.strftime("%H:%M:%S")
    today = datetime.today().strftime("%m/%d/%y")
    return f"{today}, {hours}"


def write_status_log(message, status_code='Success') -> None or Exception:
    """
    PRE: message cannot be empty
    POST: Write a api call file
    :param message: str
    :param status_code: str|int
    :return:
    """
    format_date = get_formatted_time()
    string = f"{format_date} - status code with message: {status_code} => {str(message)} \n"
    try:
        with open('status.txt', 'a') as file:
            file.write(string + '\n')
    except Exception as error:
        print(error)


def write_chat_bot(message, user='Crux') -> None or Exception:
    """

    :param message:
    :param user:
    :return:
    """
    format_date = get_formatted_time()
    string = f"{format_date}, {user}, '{message}'"
    try:
        with open('chat.txt', 'a') as file:
            file.write(string + '\n')
    except Exception as error:
        print(error)


def user_options(action, **extra_data) -> str or None or Exception:
    """

    :param action:
    :param args:
    :return:
    """
    option_file = 'r' if action == GET_NAME else 'a'
    try:
        with open('session.txt', option_file) as file:
            if 'first_time' in extra_data.keys():
                file.truncate(0)
                file.write(extra_data['name'])
            elif option_file == GET_NAME:
                return file.readline().rstrip()

    except Exception as error:
        write_status_log(error, 'Failed')
        raise Exception(error)


def remove_file(file):
    """

    :param file:
    :return:
    """
    file = os.path.abspath(file)
    if os.path.exists(file):
        if os.access(file, os.W_OK):
            try:
                os.remove(file)
            except Exception as error:
                write_status_log(error, 'Error')
                raise Exception(error)
