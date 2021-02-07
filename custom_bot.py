from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from logs import write_chat_bot, write_status_log
import facebook_bot
import instagram_bot

# The following loop will execute each time the user enters input
def run_bot(bot):
    """

    :param bot:
    :return:
    """
    start_bot = True
    is_taken_name = False
    name = ''
    while start_bot:
        try:
            if not is_taken_name:
                name = input("What's your name? ")
                is_taken_name = True
                print(f"Hi {name}!".upper())

            user_input = input("Escribi algo: ")

            bot_response = str(bot.get_response(user_input))

            if "_" in bot_response:
                exec(bot_response)
            else:
                print(bot_response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            start_bot = False


def main():
    bot = ChatBot(name='Crux')

    trainer = ListTrainer(bot)
    list_trainer = []
    try:
        with open("trainer.txt") as file:
            lines = file.readlines()
    except Exception as error:
        write_status_log(error, 'Failed')
        raise Exception(error)

    for line in lines:
        list_trainer.append(line.strip())

    trainer.train(list_trainer)

    run_bot(bot)


main()
