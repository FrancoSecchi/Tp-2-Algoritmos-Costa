from chatterbot import ChatBot
from logs import write_chat_bot
import api
from chatterbot.trainers import ListTrainer

# Create a new instance of a ChatBot
USER_TOKEN = "EAAGJNkHBQZAEBAO73ZAGv7kK71OPd3a7TSmF17OxluZBkOLKgQ8GZAvPm4J5PWUzwKdZCHrSQE2SuNmFl2lTgPcSZCY5hPbV8ZBfPElL1hkIJC2Ra7tucOf3m2Y0Qo90X9ZAfYcZBfDOfaf46CbmXQ0usEmkmg3yF8Ywr134bVeMlpJ1tJm164AmNghli50YJULkZD"



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
                if album_option in ["Ok","Yes","Y"]:
                    api.upload_to_albums(graph)
                    print("Pic uploaded! Want to do anything else? Press ctrl+c to exit")
                else:    
                    api.upload_photo(graph)
                    print("Pic uploaded! Want to do anything else? Press ctrl+c to exit")

            elif any(word in user_input for word in post_list):
                if "upload" in user_input:
                    api.upload_post(graph)
                    print("Post uploaded! Want to do anything else? Press ctrl+c to exit")
                else:
                    api.edit_post(graph)
                    print("Post edited! Want to do anything else? Press ctrl+c to exit")      
        except (KeyboardInterrupt, EOFError, SystemExit):
            start_bot = False

def bot_training(bot):
    #This are the predetermined conversations the bot can have
    trainer = ListTrainer(bot)
    greetings = [
                "Greetings",
                "Hello",
                "Hi",
                "Welcome!",
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

    error = [
             "Sorry, i did not get that",
             "What did you mean?",
             "Remember, my keywords are: Photo, Edit or Delete!"
            ]

    options = [
                "What can you do?",
                "I can help you to upload, edit or delete post or photos in your Facebook page!",
                "Help",
                "Remember to use my keywords: Photo, Edit or Delete!"
              ]

    jokes = [
             "Tell me a joke",
             "What do you call an alligator in a vest? An investigator",
             "Make me laugh",
             "What did the buffalo say to his son when he left for college? BI-son"   
            ]  

    for item in (greetings,photo,post,error,options,jokes):
        trainer.train(item)

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
    
    bot_training(bot)
    
    run_bot(bot)

main()    
