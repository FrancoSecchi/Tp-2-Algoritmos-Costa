from datetime import datetime
from termcolor import cprint
import json
import os

CHAT_FILE = "logs/chat.txt"
STATUS_FILE = "logs/status.txt"


def format_string(text: str, name: str = 'Crux') -> str:
    """
    PRE: -
    POST: Returns a string formatted with the day and time
    :return
    """
    time = datetime.now().strftime("%m/%d/%y %H:%M:%S")
    return f"{time} {name}: {text} \n"


def write_log(filename: str, text: str, username: str) -> None:
    """
    
    Returns the credentials of the test accounts, and their credentials are stored in a json
    
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
            
    except PermissionError as error:
        write_log(filename= filename, text = error.strerror, username = 'Crux')
        print_write_chat(error.strerror, color = "red")
    except Exception as e:
        write_log(filename = filename, text = str(e), username = 'Crux')
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
    except PermissionError as error:
        write_log(filename = STATUS_FILE, text = error.strerror, username = 'Crux')
        print_write_chat(error.strerror, color = "red")
    except Exception as e:
        write_log(filename = STATUS_FILE, text = str(e), username = 'Crux')
        print_write_chat(message = str(e), color = "red")


def print_write_chat(message: str, print_text: bool = True, color: str = 'white',
                     attrs_color: list = []) -> None:
    """
    
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
        cprint(message, color = color, attrs = attrs_color)
        
    write_log(filename = CHAT_FILE, text = message, username = 'Crux')


def input_user_chat(text: str) -> str:
    """
    
    :param text:
    :return:
    """
    user_name = get_username()
    user_input = input(text)
    write_log(CHAT_FILE, text = user_input, username = user_name)
    print_write_chat(message = text, print_text = False)
    
    return user_input


def get_username() -> str:
    """
    Returns the current username
    
    Arguments:
        -
    
    Returns:
        str - The current user name
    :return:
    """
    try:
        with open('logs/session.txt', 'r') as file:
            return file.readline()
    except Exception as error:
        write_log(filename = STATUS_FILE, text = str(error), username = 'Crux')
        print_write_chat(message = str(error), color = "red")


def save_username(username) -> None:
    """
    The name of the current user will be registered
    
    Arguments:
        username (str) : The name of the current user
    
    Returns:
        None
    """
    try:
        with open('logs/session.txt', 'a') as file:
            file.truncate(0)
            file.write(username)
    
    except Exception as error:
        write_log(filename = STATUS_FILE, text = str(error), username = 'Crux')
        print_write_chat(message = str(error), color = "red")


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
        bool -
    
    """
    basedir = os.path.abspath(file)
    if os.path.isfile(basedir):
        try:
            os.remove(basedir)

        except Exception as error:
            write_log(filename = STATUS_FILE, text = str(error), username = 'Crux')
            print_write_chat(message = str(error), color = "red")

