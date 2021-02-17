from apis import facebook, instagram
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from logs import write_status_log, remove_file, write_chat_bot, user_options, SAVE_USER, welcome_message
from termcolor import colored, cprint
from time import sleep
import sys


def animation(text, time = 0.025):
    """
    
    :param time:
    :param text:
    :return:
    """
    for letter in text:
        sleep(time)  # In seconds
        sys.stdout.write(letter)
        sys.stdout.flush()


def run_bot(bot):
    """

    :param bot:
    :return:
    """
    graph = facebook.connection_api()
    insta_bot = instagram.connection_instagram()
    running = True
    is_taken_name = False
    text = "Hello! I am Crux. I am the boss here. Gosh I'm sorry ... I mean bot! Oh my, I'm damned if they find out I said that ... \nAh, well, before Elon Musk finds me and sends me to Mars.\n"
    animation(text)
    subtitle = colored("There's something I want to tell you.\n", 'blue', attrs = ['bold', 'underline'])
    animation(subtitle)
    write_chat_bot(text + " " + "There's something I want to tell you.\n")
    
    welcome_message()
    cprint("PLEASE READ ALL THE MESSAGE, thanks :D", 'blue', attrs=['bold', 'underline', 'blink'])
    write_chat_bot("PLEASE READ ALL THE MESSAGE, thanks :D")
    
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
            
            user_input = input("\nYou: ")
            write_chat_bot(user_input, name)
            
            bot_response = str(bot.get_response(user_input))
            if "_" in bot_response:
                exec(bot_response)
            else:
                print(bot_response)
                write_chat_bot(bot_response)
        
        except (KeyboardInterrupt, EOFError, SystemExit):
            animation("\nMay the Force be with you\n")
            write_chat_bot("May the Force be with you")
            running = False


def main():
    bot = ChatBot(name = 'Crux')
    trainer = ListTrainer(bot)
    list_trainer = []
    remove_file('status.txt')
    remove_file('chat.txt')
    try:
        with open("trainer.txt") as file:
            lines = file.readlines()
    
    except Exception as error:
        write_status_log('Failed', error)
        raise Exception(error)
    
    for line in lines:
        list_trainer.append(line.strip())
    
    trainer.train(list_trainer)
    run_bot(bot)


main()
