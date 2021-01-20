from datetime import datetime


def getFormattedTime() -> str:
    now = datetime.now()
    hours = now.strftime("%H:%M:%S")
    today = datetime.today().strftime("%m/%d/%y")
    return f"{today}, {hours}"


def writeStatusLog(message, status_code='Success'):
    """
    PRE: message cannot be empty
    POST: Write a api call file
    :param message:
    :param status_code:
    :return:
    """
    format_date = getFormattedTime()
    string = f"{format_date} - status code with message: {status_code} => {message} \n"
    with open('status.txt', 'a') as file:
        file.write(string + '\n')


def writeChatBot(user, message):
    format_date = getFormattedTime()
    string = f"{format_date}, {user}, '{message}'"
    with open('chat.txt', 'a') as file:
        file.write(string + '\n')
