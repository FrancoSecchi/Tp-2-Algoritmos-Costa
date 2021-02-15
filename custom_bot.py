from apis import facebook, instagram
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from logs import write_status_log, remove_file , write_chat_bot, user_options, SAVE_USER


def run_bot(bot):
    """

    :param bot:
    :return:
    """
    #graph = facebook.connection_api()
    insta_bot = instagram.connection_instagram()
    running = True
    is_taken_name = False
    while running:
        try:
            if not is_taken_name:
                name = input("What's your name? ")
                write_chat_bot("What's your name? ")
                write_chat_bot(name, name)
                is_taken_name = True
                print(f"Hi {name}!")
                write_chat_bot(f"Hi {name}!")
                user_options(SAVE_USER, name=name, first_time=True)

            user_input = input("You: ")

            bot_response = str(bot.get_response(user_input))

            if "_" in bot_response:
                exec(bot_response)
            else:
                print(bot_response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            running = False


def main():
    bot = ChatBot(name='Crux')
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
        if "<" not in line or ">" not in line:
            list_trainer.append(line.strip())

    trainer.train(list_trainer)

    run_bot(bot)


main()
