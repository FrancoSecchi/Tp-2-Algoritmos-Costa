from datetime import datetime


def get_formatted_time() -> str:
    now = datetime.now()
    hours = now.strftime("%H:%M:%S")
    today = datetime.today().strftime("%m/%d/%y")
    return f"{today}, {hours}"


def write_status_log(message, status_code='Success'):
    """
    PRE: message cannot be empty
    POST: Write a api call file
    :param message: str
    :param status_code: str|int
    :return:
    """
    format_date = get_formatted_time()
    string = f"{format_date} - status code with message: {status_code} => {str(message)} \n"
    with open('status.txt', 'a') as file:
        file.write(string + '\n')


def write_chat_bot(user, message):
    format_date = get_formatted_time()
    string = f"{format_date}, {user}, '{message}'"
    try:
        with open('chat.txt', 'a') as file:
            file.write(string + '\n')
    except FileExistsError as error:
        write_status_log(500, str(error))
        print(f"Error: {error}")
