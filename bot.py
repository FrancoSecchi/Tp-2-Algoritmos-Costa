from chatterbot import ChatBot
from logs import write_chat_bot
import api

# Create a new instance of a ChatBot


print('Type something to begin...')


# The following loop will execute each time the user enters input
def run_bot(bot):
    """

    :param bot:
    :return:
    """
    start_bot = True
    while start_bot:
        try:
            user_input = input()

            bot_response = bot.get_response(user_input)

            print(bot_response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            start_bot = False


def main():
    bot = ChatBot(
        'Terminal',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation',
            'chatterbot.logic.TimeLogicAdapter',
            'chatterbot.logic.BestMatch'
        ],
        database_uri='sqlite:///database.db'
    )
    run_bot(bot)
