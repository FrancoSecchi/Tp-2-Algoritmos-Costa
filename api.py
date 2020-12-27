from pyfacebook import Api
import json  # Use the json module to write the files

APP_ID = "432341101134225"
KEY_SECRET = "5f1a24aa9fc8ebd8f6e5cd26a1603ac3"
PAGE_ID = "108139397867813"
ACCESS_TOKEN = "EAAFotLIb7ZBwBADv62AN2B1zTgji8HZC8wOcM3fAzoFt22eu637VLoSlPagZCIAE3P6Xz0SB6LPC7nGQZBDukejsynb1xa56sediPEVASl2orQjBNEZCs4LxpCzlb8u2IW1iCFAdUt4z8Vl1Kz1dFIpQVo60dZBtILIyqF4j2E4mtyUT55MF1K0aF5OYLLgdNtEc5bOOwXF9Wb6S9Dy3c40ozzJHlFJk6Jw0ganbgp5wZDZD"

# TODO Declare the necessary functions to carry out the draft


def connection():
    try:
        api = Api(app_id=APP_ID, app_secret=KEY_SECRET, long_term_token=ACCESS_TOKEN)
        return api, True
    except Exception as error:
        print(error)


def processor():
    data, isConnected = connection()
    if isConnected:
        print(data.get_token_info())


processor()
