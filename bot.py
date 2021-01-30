from chatterbot import ChatBot
from logs import write_chat_bot
import api
from chatterbot.trainers import ListTrainer

# Create a new instance of a ChatBot
USER_TOKEN = "EAAGJNkHBQZAEBAIMMz78M1ZArgjk1IiP4asgl72V0PtbxZAIVIzVhjc0L3xXenU3awpLI3exj5T8sK8XPqjLZBXEUtjFhy8HJumudDIAJUYeRti57d13764IV2LL7tn2YldrF8TCiTzqIXF2YH9Kk4PUQQheRP6M9x5oddQn9oiQ4Blsgs1noYf6QozpW70Fw06gPevV5AZDZD"

print('Type something to begin...')


# The following loop will execute each time the user enters input
def run_bot(bot):
    """

    :param bot:
    :return:
    """
    photo_list = ["photo","pic","image"]
    post_list = ["post","edit","delete"]
    graph = api.connectionApi(user_token=USER_TOKEN)
    start_bot = True
    while start_bot:
        try:
            user_input = input()

            bot_response = bot.get_response(user_input)
            print(bot_response)
            
            if any(word in user_input for word in photo_list):
                album_option = input ("Would you like to upload the photo to an album?\n").capitalize()
                if album_option == "Yes" or album_option == "Ok":
                    api.upload_to_albums(graph)
                else:    
                    api.upload_photo(graph)

            elif any(word in user_input for word in post_list):
                if "upload" in user_input:
                    api.upload_post(graph)
                else:
                    api.edit_post(graph)    
        except (KeyboardInterrupt, EOFError, SystemExit):
            start_bot = False


def main():
    bot = ChatBot(
        'Crux',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation',
            'chatterbot.logic.BestMatch'
        ],
        database_uri='sqlite:///database.db'
    )
    bot.storage.drop()
    trainer = ListTrainer(bot)
    greetings = [
                "Greetings",
                "Hello",
                "Hi",
                "How can i help you?",
                "Crux",
                "At your service!"
                ]

    photo = [
            "I want to upload a photo",
            "On it",
            "Upload pic", 
            "On it!",
            ]
    
    post = [
            "I want to upload a post",
            "Great",
            "Edit post",
            "Alright",
            "Delete post",
            "Ok"
            ]
    for item in (greetings,photo):
        trainer.train(item)
    run_bot(bot)

main()    
