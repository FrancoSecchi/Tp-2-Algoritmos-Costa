import os
import json
import sys
import time
from time import sleep
from logs import (write_log, STATUS_FILE, print_write_chatbot)


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


def get_credentials():
    """
    Returns the credentials of the test accounts, and their credentials are stored in a json
    
    Returns:
        Dict - Dictionary in which the credentials are found
    """
    try:
        with open("credentials/crux_credentials.json", 'r') as file:
            return json.load(file)
    except Exception as e:
        write_log(filename = STATUS_FILE, text = str(e), username = 'Exception')
        print_write_chatbot(message = str(e), color = "red")


def save_username(username: str) -> None:
    """
    The name of the current user will be registered

    Arguments:
        username (str) : The name of the current user

    Returns:
        None
    """
    try:
        with open('logs/session.txt', 'w') as file:
            file.truncate(0)
            file.write(username)
    except Exception as error:
        write_log(filename = STATUS_FILE, text = str(error), username = 'Exception')
        print_write_chatbot(message = str(error), color = "red", attrs_color = ['bold'])


def welcome_message() -> None:
    """
    Print by console the welcome message to the user,
     which informs which are the available functionalities of the bot
    """
    try:
        with open('welcome_message.txt', 'r') as file:
            lines = file.readlines()
        text = ''
        for line in lines:
            text += line.strip('\n') + "\n"
        print_write_chatbot(text)
    except Exception as error:
        write_log(filename = STATUS_FILE, text = str(error), username = 'Exception')
        print_write_chatbot(message = str(error), color = "red")


def delete_file(file: str) -> None:
    """
    Delete the file that is passed by parameter

    Arguments:
        file (str): The relative path of the file to delete
    """
    basedir = os.path.abspath(file)
    
    if os.path.exists(basedir):
        try:
            os.remove(basedir)
        except Exception as error:
            write_log(filename = STATUS_FILE, text = str(error), username = 'Exception')
            print_write_chatbot(message = str(error), color = "red")


def get_current_username(first_time = False) -> str:
    """
    Returns the current username

    Arguments:
        first_time (bool) : This indicates if the first time the user is asked for input
                            (This is done exclusively before asking for the name)

    Returns:
        str - The current user name
    """
    if not first_time:
        try:
            with open('logs/session.txt', 'r') as file:
                return file.readline()
        except Exception as error:
            write_log(filename = STATUS_FILE, text = str(error), username = 'Crux')
            print_write_chatbot(message = str(error), color = "red")
            return "Unknown"
    else:
        return 'Unknown'


def animation(text: str) -> None:
    """
    Make an animation by printing a text like a typewriter to give dynamism to the console
    Arguments:
        text (str) = Text to animate
    """
    for letter in text:
        sleep(0.025)  # In seconds
        sys.stdout.write(letter)
        sys.stdout.flush()


def delete_expired_cookie(file: str) -> None:
    """
    If more than 1 hour has passed, the cookie will be deleted to avoid errors

    Arguments:
        file (str) : The relative path of the cookie file
    """
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        create_time = data['created_ts']
        now = time.time()
        if (create_time + 3600) <= round(now):
            delete_file(file)
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Exception')
        print(f"There was an error:{error}")

