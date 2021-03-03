import os
from termcolor import colored
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from apis import facebook, instagram
from logs import print_write_chatbot, input_user_chat, write_log, STATUS_FILE
from utils.utils import user_answer_is_yes, animation, delete_file, welcome_message, save_username


def connection_facebook_api() -> object:
    """
    The user is asked if he has an facebook page to connect, if he does not have, the Crux account will be used

    Returns:
         object (facebook.GraphAPI()) - facebook.GraphAPI object
    """
    response = input_user_chat("Would you like to connect to Facebook? (yes/no): ")
    credentials = {}

    if user_answer_is_yes(response.lower()):
        page_token = input_user_chat("Please enter your page access token: ")
        credentials = {'token': page_token}
    else:
        print_write_chatbot("By not using the facebook tool with your personal page, "
                            "we will provide the service with our"
                            "Facebook page Crux.cruz", color = 'blue', attrs_color = ['bold'])
    
    facebook_api = facebook.connection_api(user_credentials = credentials)
    return facebook_api


def connection_instagram_api() -> object:
    """
    The user is asked if he has an instagram account to connect,
     if he does not have, the Crux account will be used
          
    Returns:
         object (instagram.Client()) - instagram.Client object
    """
    response = input_user_chat("Would you like to connect to Instagram? (yes/no): ")
    credentials = {}
    if user_answer_is_yes(response.lower()):
        username = input_user_chat("Please enter your username: ")
        password = input_user_chat("Please enter your password: ")
        
        credentials = {
                'username': username,
                'password': password
            }
    else:
        print_write_chatbot("By not using the instagram tool with your personal page,"
                            " we will provide the service with our Instagram account crux.bot",
                            color = 'blue', attrs_color = ['bold'])
        
    instagram_api = instagram.connection_instagram(user_credentials = credentials)
    
    return instagram_api


def print_welcome_message() -> None:
    """
    Prints the welcome message of Crux with effects
    """
    text = "Hello! I am Crux. I am the boss here. Gosh I'm sorry ... " \
           "I mean bot! Oh my, I'm damned if they find out" \
           " I said that ... \nAh, well, before Elon Musk finds me and sends me to Mars.\n"
    animation(text)
    subtitle = colored("There's something I want to tell you.\n", 'blue',
                       attrs = ['bold', 'underline'])
    animation(subtitle)
    print_write_chatbot(text + subtitle, print_text = False)
    
    welcome_message()


def ask_name() -> True:
    """
    Ask the user for his/her name
    """
    name = input_user_chat("What's your name? ", first_time = True)
    print_write_chatbot(f"Hi {name}!")
    save_username(name)
    return True


def run_bot(bot: ChatBot) -> None:
    """
    The user interacts with the bot. The bot can answer the user or execute the functions requested by the user
    Arguments:
        bot (ChatBot)
    
    """
    print_welcome_message()
    running = True
    is_taken_name = False
    read = False
    while not read:
        print_write_chatbot("PLEASE READ ALL THE MESSAGE",
                            color = 'blue',
                            attrs_color = ['bold', 'underline', 'blink'])
        
        is_read = input_user_chat("Did you read all the message? (yes/no) ", first_time = True)
        read = user_answer_is_yes(is_read)
    
    while running:
        try:
            
            if not is_taken_name:
                is_taken_name = ask_name()
                facebook_api, instagram_api = connection_facebook_api(), connection_instagram_api()
            
            user_input = input_user_chat("\nYou: ")
            bot_response = str(bot.get_response(user_input))
            
            if "_" in bot_response:
                exec(bot_response)
            else:
                print_write_chatbot(bot_response)
            
            keep_running = input_user_chat("Do you want to continue chatting with me?? (yes/no): ")
            
            if not user_answer_is_yes(keep_running):
                running = False
        
        except (KeyboardInterrupt, EOFError, SystemExit):
            running = False
    else:
        print_write_chatbot("It's the end", color = 'blue', attrs_color = ['bold'])
        animation("May the Force be with you\n")
        print_write_chatbot("May the Force be with you", print_text = False)


def is_already_trained() -> bool:
    """
    Check if the bot's database already exists, if it exists, it means that the bot is trained and vice versa

    Returns:
        bool - Returns True if the bot is trained, otherwise it returns false
    """
    path_file = os.path.abspath("database.db")
    return True if os.path.isfile(path_file) else False


def train_bot(bot) -> None:
    """
    The txt containing the training is read and trains the bot
    
    Arguments:
        bot (ChatBot) : ChatBot object
 
    """
    
    trainer = ListTrainer(bot)
    list_trainer = []
    try:
        with open("trainer.txt") as file:
            lines = file.readlines()
    
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Crux')
        print_write_chatbot(str(error))
    
    for line in lines:
        list_trainer.append(line.strip())
    
    trainer.train(list_trainer)


def initialize_bot():
    """
    Starts the bot
    """
    return ChatBot(
        name = 'Crux',
        storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
        logic_adapters = [
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.9
            },
        ],
        database_uri = 'sqlite:///database.db'
    )


def main():
    for file in ['logs/chat.txt', 'logs/session.txt']:
        delete_file(file)
    
    if not is_already_trained():
        bot = initialize_bot()
        train_bot(bot)
    else:
        bot = initialize_bot()
    
    run_bot(bot)


main()
