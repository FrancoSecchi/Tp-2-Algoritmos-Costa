import os
import sys
from time import sleep
from termcolor import colored, cprint
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from apis import facebook, instagram
from logs import delete_file, save_username, \
    welcome_message, print_write_chat, input_user_chat, write_log, STATUS_FILE
from utils.utils import user_answer_is_yes


def animation(text: str) -> None:
    """
    Make an animation by printing a text like a typewriter to give dynamism to the console
    Arguments:
        text (str) = Text to animate
    Returns:
        None
    """
    for letter in text:
        sleep(0.025)  # In seconds
        sys.stdout.write(letter)
        sys.stdout.flush()


def facebook_credentials():
    """
    The user is asked if he has an facebook page to connect,
     if he does not have, the Crux account will be used
    
    Arguments:
        -
        
    Returns:
         object (facebook.GraphAPI()) - facebook.GraphAPI object
    """
    response = input_user_chat("\nWould you like to connect to Facebook? (yes/no): ")
    if user_answer_is_yes(response.lower()):
        page_token = input_user_chat("\nPlease enter your page access token: ")
        facebook_api = facebook.connection_api(
            user_credentials = {
                'token': page_token
            }
        )
    else:
        print_write_chat("\nBy not using the facebook tool with your personal page, "
                         "we will provide the service with our"
                         "Facebook page Crux.cruz", color = 'blue', attrs_color = ['bold'])
        facebook_api = facebook.connection_api()
    return facebook_api


def instagram_credentials():
    """
    The user is asked if he has an instagram account to connect,
     if he does not have, the Crux account will be used
    
    Arguments:
        -
        
    Returns:
         object (instagram.Client()) - instagram.Client object
    """
    response = input_user_chat("\nWould you like to connect to Instagram? (yes/no): ")
    
    if user_answer_is_yes(response.lower()):
        username = input_user_chat("\nPlease enter your username: ")
        password = input_user_chat("\nPlease enter your password: ")
        
        instagram_api = instagram.connection_instagram(
            user_credentials = {
                'username': username,
                'password': password
            }
        )
    else:
        instagram_api = instagram.connection_instagram()
        print_write_chat("By not using the instagram tool with your personal page,"
                         " we will provide the service with our Instagram account crux.bot",
                         color = 'blue', attrs_color = ['bold'])
    
    return instagram_api


def run_bot(bot) -> None:
    """
    Arguments:
        bot (ChatBot)
    """
    running = True
    is_taken_name = False
    text = "Hello! I am Crux. I am the boss here. Gosh I'm sorry ... " \
           "I mean bot! Oh my, I'm damned if they find out" \
           " I said that ... \nAh, well, before Elon Musk finds me and sends me to Mars.\n"
    animation(text)
    subtitle = colored("There's something I want to tell you.\n", 'blue',
                       attrs = ['bold', 'underline'])
    animation(subtitle)
    print_write_chat(text + subtitle, print_text = False)
    
    welcome_message()
    read = False
    while not read:
        print_write_chat("\nPLEASE READ ALL THE MESSAGE",
                         color = 'blue',
                         attrs_color = ['bold', 'underline', 'blink'])
        
        is_read = input_user_chat("Did you read all the message? (yes/no) ")
        read = user_answer_is_yes(is_read)
    
    while running:
        try:
            if not is_taken_name:
                name = input_user_chat("\nWhat's your name? ")
                is_taken_name = True
                print_write_chat(f"Hi {name}!")
                save_username(name)
                graph, instagram_api = facebook_credentials(), instagram_credentials()
            
            user_input = input_user_chat("\nYou: ")
            bot_response = str(bot.get_response(user_input))
            
            if "_" in bot_response:
                exec(bot_response)
            else:
                print_write_chat(bot_response)
            
            keep_running = input("Do you want to continue chatting with me?? (yes/no) ")
            
            if user_answer_is_yes(keep_running):
                running = False
        
        except (KeyboardInterrupt, EOFError, SystemExit):
            running = False
            print_write_chat("It's the end", color = 'blue', attrs_color = ['bold'])
    else:
        animation("\nMay the Force be with you\n")
        print_write_chat("May the Force be with you", print_text = False)


def is_already_trained() -> bool:
    """
    Check if the bot's database already exists, if it exists, it means that the bot is trained and vice versa

    Arguments:
        -

    Returns:
        bool - Returns True if the bot is trained, otherwise it returns false
    """
    path_file = os.path.abspath("db.sqlite3")
    return True if os.path.isfile(path_file) else False


def train_bot(bot) -> None:
    """
    The txt containing the training is read and trains the bot
    
    Arguments:
        bot (ChatBot) : ChatBot object
    
    Returns:
        None
    """
    
    trainer = ListTrainer(bot)
    list_trainer = []
    try:
        with open("trainer.txt") as file:
            lines = file.readlines()
    
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Crux')
        print_write_chat(str(error))
    
    for line in lines:
        list_trainer.append(line.strip())
    
    trainer.train(list_trainer)


def main():
    delete_file('logs/status.txt')
    delete_file('logs/chat.txt')
    bot = ChatBot(
        name = 'Crux',
        storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
        logic_adapters = [
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.80
            }
        ],
    )
    if not is_already_trained():
        train_bot(bot)
    
    run_bot(bot)


main()
