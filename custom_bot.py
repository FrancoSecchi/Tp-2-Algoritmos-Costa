import os

from apis import facebook, instagram
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from logs import write_status_log, remove_file, write_chat_bot, user_options, SAVE_USER, welcome_message
from termcolor import colored, cprint
from time import sleep
import json
import sys


def animation(text, time = 0.025):
    """
    PRE: the text parameter cant be null
    POST: Make an animation by printing a text like a typewriter to give dynamism to the console
    :param time:
    :param text:
    :return:
    """
    for letter in text:
        sleep(time)  # In seconds
        sys.stdout.write(letter)
        sys.stdout.flush()


def access(name):
    """
    PRE: The parameter cant be null, and its the user name
    POS: Returns the connections selected by the user
    """
    response = input("\nWould you like to connect to Facebook? (yes/no): ").lower()
    if response in ["yes", 'ye', 'y']:
        page_token = input("\nPlease enter your page access token: ")
        write_chat_bot("Please enter your page access token: ")
        write_chat_bot(page_token, name)
        graph = facebook.connection_api(token = page_token)
    else:
        cprint("\nBy not using the facebook tool with your personal page, we will provide the service with our Facebook page Crux.cruz", 'blue', attrs = ['bold'])
        write_chat_bot("By not using the facebook tool with your personal page, we will provide the service with our Facebook page Crux.cruz")
        graph = facebook.connection_api()
    
    ig_response = input("Would you like to connect to Instagram? (yes/no): ").lower()
    write_chat_bot("Would you like to connect to Instagram? (yes/no): ")
    write_chat_bot(ig_response, name)
    if ig_response == ["yes", 'ye', 'y']:
        username = input("\nPlease enter your username: ")
        password = input("\nPlease enter your password: ")
        write_chat_bot("Please enter your username: ")
        write_chat_bot(username, name)
        write_chat_bot("Please enter your password: ")
        write_chat_bot(password, name)
        insta_api = instagram.connection_instagram(username = username, password = password)
    else:
        insta_api = instagram.connection_instagram()
        cprint("\nBy not using the instagram tool with your personal page, we will provide the service with our Instagram account crux.bot", 'blue', attrs = ['bold'])
        write_chat_bot("By not using the instagram tool with your personal page, we will provide the service with our Instagram account crux.bot")
    
    return graph, insta_api


def run_bot(chat_bot):
    """
    PRE: The chat_bot cant be null
    POST: The conversation with the bot is executed
    :param chat_bot:
    :return:
    """
    running = True
    is_taken_name = False
    text = "Hello! I am Crux. I am the boss here. Gosh I'm sorry ... I mean bot! Oh my, I'm damned if they find out I said that ... \nAh, well, before Elon Musk finds me and sends me to Mars.\n"
    animation(text)
    subtitle = colored("There's something I want to tell you.\n", 'blue', attrs = ['bold', 'underline'])
    animation(subtitle)
    write_chat_bot(text + " " + "There's something I want to tell you.\n")
    
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
                user_options(SAVE_USER, name = name, first_time = True)
                graph, insta_api = access(name)
            
            user_input = input("\nYou: ")
            write_chat_bot(user_input, name)
            
            bot_response = str(chat_bot.get_response(user_input))
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


def main():
    chat_bot = ChatBot(
        name = 'Crux',
        storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
        logic_adapters = [
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.90
            }
        ],
        database_uri = 'sqlite:///database.db'
    )
    trainer = ListTrainer(chat_bot)
    list_trainer = []
    remove_file('logs/status.txt')
    remove_file('logs/chat.txt')
    try:
        with open("trainer.txt") as file:
            lines = file.readlines()
    
    except Exception as error:
        write_status_log(error, 'Exception')
        raise Exception(error)
    
    for line in lines:
        list_trainer.append(line.strip())
    
    trainer.train(list_trainer)
    run_bot(chat_bot)


main()
