from datetime import datetime

from apis import facebook, instagram
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from logs import delete_file, save_username, welcome_message, print_write_chat
from utils.utils import user_answer_is_yes
from time import sleep
import os
import sys
from termcolor import colored, cprint


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


def is_already_trained():
    """
    
    :return:
    """
    path_file = os.path.abspath("db.sqlite3")
    return True if os.path.isfile(path_file) else False


def facebook_credentials():
    """
    
    :return:
    """
    response = input("\nWould you like to connect to Facebook? (yes/no): ").lower()
    if user_answer_is_yes(response):
        page_token = input("\nPlease enter your page access token: ")
        write_chat_bot("Please enter your page access token: ")
        write_chat_bot(page_token, name)
        facebook_api = facebook.connection_api(
            user_credentials = {
                'token': page_token
            }
        )
    else:
        cprint(
            "\nBy not using the facebook tool with your personal page, we will provide the service with our "
            "Facebook page Crux.cruz",
            'blue', attrs = ['bold'])
        write_chat_bot(
            "By not using the facebook tool with your personal page, we will provide the service with our Facebook "
            "page Crux.cruz")
        facebook_api = facebook.connection_api()
    return facebook_api


def instagram_credentials():
    """
    PRE: The parameter cant be null, and its the user name
    POS: Returns the connections selected by the user
    """
    response = input("Would you like to connect to Instagram? (yes/no): ").lower()
    
    if user_answer_is_yes(response):
        username = input("\nPlease enter your username: ")
        password = input("\nPlease enter your password: ")
        
        instagram_api = instagram.connection_instagram(
            user_credentials = {
                'username': username,
                'password': password
            }
        )
    else:
        instagram_api = instagram.connection_instagram()
        cprint(
            "\nBy not using the instagram tool with your personal page, we will provide the service with our Instagram account crux.bot",
            'blue', attrs = ['bold'])
        write_chat_bot(
            "By not using the instagram tool with your personal page, we will provide the service with our Instagram account crux.bot")
    
    return instagram_api


def run_bot(bot):
    """
    PRE: The chat_bot cant be null
    POST: The conversation with the bot is executed
    :param bot:
    :return:
    """
    running = True
    is_taken_name = False
    text = "Hello! I am Crux. I am the boss here. Gosh I'm sorry ... I mean bot! Oh my, I'm damned if they find out" \
           " I said that ... \nAh, well, before Elon Musk finds me and sends me to Mars.\n"
    animation(text)
    subtitle = colored("There's something I want to tell you.\n", 'blue',
                       attrs = ['bold', 'underline'])
    animation(subtitle)
    
    welcome_message()
    read = False
    while not read:
        cprint("\nPLEASE READ ALL THE MESSAGE", 'blue', attrs = ['bold', 'underline', 'blink'])
        write_chat_bot("PLEASE READ ALL THE MESSAGE")
        is_read = input("Did you read all the message? (yes/no) ")
        write_chat_bot("Did you read all the message? (yes/no)")
        write_chat_bot(is_read, 'Unknown')
        read = is_read.lower() in ['yes', 'ye', 'y']
    
    name = ''
    while running:
        try:
            if not is_taken_name:
                name = input("\nWhat's your name? ")
                write_chat_bot("What's your name? ")
                write_chat_bot(name, name)
                is_taken_name = True
                print(f"\nHi {name}!")
                write_chat_bot(f"Hi {name}!")
                save_username(name)
                graph, instagram_api = facebook_credentials(), instagram_credentials()
            
            user_input = input("\nYou: ")
            write_chat_bot(user_input, name)
            
            bot_response = str(bot.get_response(user_input))
            if "_" in bot_response:
                exec(bot_response)
            else:
                print(bot_response)
                write_chat_bot(bot_response)
            
            running = input("Do you want to continue chatting with me?? (yes/no) ")
            write_chat_bot("Do you want to continue chatting with me?? (yes/no) ")
            write_chat_bot(running, name)
            if running.lower() not in ['yes', 'ye', 'y']:
                running = False
        
        except (KeyboardInterrupt, EOFError, SystemExit):
            running = False
            write_chat_bot("It's the end", 'SystemExit')
    else:
        animation("\nMay the Force be with you\n")
        write_chat_bot("May the Force be with you")


def train_bot(bot):
    """
    
    :param bot:
    :return:
    """
    
    trainer = ListTrainer(bot)
    list_trainer = []
    try:
        with open("trainer.txt") as file:
            lines = file.readlines()
    
    except Exception as error:
        write_status_log(error, 'Exception')
        raise Exception(error)
    
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
    
    exit()
    run_bot(bot)


main()
