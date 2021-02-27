import json
import os
from datetime import datetime
from termcolor import cprint

CHAT_FILE = "logs/chat.txt"
STATUS_FILE = "logs/status.txt"


def format_string(text: str, name: str = 'Crux') -> str:
    """
    A text is constructed with the format of (time) (name): (text),  to save them in the logs
    
    Arguments:
        text (str) : The user / bot generated text
        name (str) : The name of the user who wrote the text
    
    Returns:
        str - Formatted string (time) (name): (text)
    """
    time = datetime.now().strftime("%m/%d/%y %H:%M:%S")
    return f"{time} {name}: {text} \n"


def write_log(filename: str, text: str, username: str) -> None:
    """
    Write or create a txt file that will save a specific text for a user,
    and the txt will be saved in the carpet logs/
    
    Arguments:
        filename (str) : The relative path of the file to update
        text (str) :  Text to be written to the file
        username (str) :
    
    Returns:
        Dict - Dictionary in which the credentials are found
    """
    string_formatted = format_string(text, username)
    try:
        with open(filename, 'a') as file:
            file.write(string_formatted)
    except Exception as e:
        print_write_chat(message = str(e), color = "red")


def get_credentials():
    """
    Returns the credentials of the test accounts, and their credentials are stored in a json
    
    Arguments:
        -
    
    Returns:
        Dict - Dictionary in which the credentials are found
    """
    try:
        with open("credentials/crux_credentials.json", 'r') as file:
            return json.load(file)
    except Exception as e:
        write_log(filename = STATUS_FILE, text = str(e), username = 'Crux')
        print_write_chat(message = str(e), color = "red")


def print_write_chat(message: str, print_text: bool = True, color: str = 'white',
                     attrs_color: list = []) -> None:
    """
    A text is printed on the screen and that same text will be saved in the chat log
    
    Arguments:
        message (str) : Message to display
        print_text (bool) : Indicates if the text has to be printed,
                            it is used in the case that a text is being printed through the input_user_chat function
                            (default True)
        color (str) : The color of the text to display (default "white")
        attrs_color (list) : Contains the available attributes for the text style.
                            Eg ['bold', 'blink' 'underline', etc] (default [])
        
    Returns:
        None
    """
    if print_text:
        cprint("\n" + message, color = color, attrs = attrs_color)
    
    write_log(filename = CHAT_FILE, text = message, username = 'Crux')


def input_user_chat(text: str, first_time = False) -> str:
    """
    The user is asked for a specific input, the input is recorded in the logs, and the input value is returned
    
    Arguments:
        text (str) : Text that will indicate what value the user must enter
        first_time (bool) : This indicates if the first time the user is asked for input
                            (This is done exclusively before asking for the name)
    Returns:
        str - The value of the input given by the user
    """
    user_name = get_username(first_time)
    user_input = input("\n" + text)
    write_log(CHAT_FILE, text = user_input, username = user_name)
    print_write_chat(message = text, print_text = False)
    return user_input


def get_username(first_time = False) -> str:
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
            print_write_chat(message = str(error), color = "red")
    else:
        return 'Unknown'


def save_username(username) -> None:
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
        write_log(filename = STATUS_FILE, text = str(error), username = 'Crux')
        print_write_chat(message = str(error), color = "red", attrs_color = ['bold'])


def welcome_message() -> None:
    """
    Print by console the welcome message to the user,
     which informs which are the available functionalities of the bot
    
    Arguments:
        -
        
    Returns:
        None
    """
    try:
        with open('welcome_message.txt', 'r') as file:
            lines = file.readlines()
        text = ''
        for line in lines:
            text += line.strip('\n') + "\n"
        print_write_chat(text)
    except Exception as error:
        write_log(filename = STATUS_FILE, text = str(error), username = 'Crux')
        print_write_chat(message = str(error), color = "red")


def delete_file(file: str) -> None:
    """
    Delete the file that is passed by parameter
    
    Arguments:
        file (str): The relative path of the file to delete
    
    Returns:
        None
    """
    basedir = os.path.abspath(file)
    
    if os.path.exists(basedir):
        try:
            os.remove(basedir)

        except Exception as error:
            write_log(filename = STATUS_FILE, text = str(error), username = 'Crux')
            print_write_chat(message = str(error), color = "red")
    