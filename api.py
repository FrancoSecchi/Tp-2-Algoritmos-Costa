from pyfacebook import Api
import json  # Use the json module to write the files

APP_ID = "432341101134225"
KEY_SECRET = "5f1a24aa9fc8ebd8f6e5cd26a1603ac3"  # The key changes through the time, check the app in facebook.developers
PAGE_ID = "103914631637231"
ACCESS_TOKEN = "EAAGJNkHBQZAEBAL8bEZARl3Q3GZCMNukGegto3gU9f8XNuxbreju755xKZATHwI389SMdh09qYZAZBZAZCxZAWhQFHoDEhqLME3OXRRJZAENytaOSl3HH08H8Qee92PF2bdvdAxmGNNFswyKdi5yu9wLawO7INU5ytSSAZA35XH2PLUtS2sZAvRZAzgJcwbZBH4GTuvGi1RcCZAyp89QgZDZD" # The key changes through the time, check the app in facebook.developers

# TODO Declare the necessary functions to carry out the draft


def connection():
    try:
        api = Api(app_id=APP_ID, app_secret=KEY_SECRET, long_term_token=ACCESS_TOKEN)
        return api, True
    except ConnectionError as error:
        print(f'Problemas de conexion: {error}')
    except Exception as error:
        print(error)


def main():
    data, isConnected = connection()
    if isConnected:
        print(data.get_token_info())


main()
