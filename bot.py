from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from logs import write_chat_bot
import api

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

            if "(" in bot_response or ")" in bot_response:
                exec(bot_response)
            else:
                print(bot_response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            start_bot = False


def main():
    bot = ChatBot(name='Crux')

    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train('./trainer.yml')

    run_bot(bot)


main()
