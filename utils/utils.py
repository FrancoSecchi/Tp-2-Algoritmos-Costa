import codecs
import os
import json
import sys
import time
from time import sleep
from logs import (write_log, STATUS_FILE, print_write_chatbot)
from instagram_private_api import Client


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


def to_json(python_object: bytes) -> dict:
    """
    Returns a dictionary indicating that the json
    value is in bytes and makes a decode of the bytes that are in base64

    Arguments:
        python_object (bytes)
    Returns:
        dict
    """
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object: dict):
    """
    In the case that the json object is in bytes, it returns a decode of the bytes in base64
    Arguments:
        json_object (dict)

    Returns:

    """
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def on_login_callback(api: Client, new_settings_file: str) -> None:
    """
    Write, in a json, the cookies and settings to avoid re-login

    Arguments:
        api (Client): the actual Client object
        new_settings_file (str): The json file where the credentials will be saved
    """
    cache_settings = api.settings
    try:
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default = to_json)
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Exception')
        print(f"There was an error:{error}")


def get_cached_settings(settings_file) -> dict:
    """
    Returns cached bot settings
    Arguments:
        settings_file (str)
    """
    try:
        with open(settings_file) as file_data:
            cached_settings = json.load(file_data, object_hook = from_json)
        return cached_settings
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Exception')
        print(f"There was an error:{error}")
