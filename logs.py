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
        print_write_chatbot(message = str(e), color = "red")


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


def print_write_chatbot(message: str, print_text: bool = True, color: str = 'white',
                        attrs_color: list = []) -> None:
    """
    A text is printed on the screen and that same text will be saved in the chat log
    
    Arguments:
        message (str) : Message to display
        print_text (bool) : Indicates if the text has to be printed,
                            it is used in the case that a text
                            is being printed through the input_user_chat function
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
    The user is asked for a specific input, the input is recorded in the logs,
    and the input value is returned
    
    Arguments:
        text (str) : Text that will indicate what value the user must enter
        first_time (bool) : This indicates if the first time the user is asked for input
                            (This is done exclusively before asking for the name)
    Returns:
        str - The value of the input given by the user
    """
    user_name = get_current_username(first_time)
    user_input = input("\n" + text)
    print_write_chatbot(message = text, print_text = False)
    write_log(CHAT_FILE, text = user_input, username = user_name)
    return user_input
