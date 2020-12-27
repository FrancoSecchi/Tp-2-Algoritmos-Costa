from pyfacebook import Api
import json  # Use the json module to write the files

APP_ID = "396600268287980"
KEY_SECRET = "c5b4c791b1dc437544ff45af562410ac"  # The key changes through the time, check the app in facebook.developers
PAGE_ID = "108139397867813"
ACCESS_TOKEN = "EAAFotLIb7ZBwBAIKp9NX4TxZCI8tPUkCY7KekrQwqj3mv2zJRnTQjxrprHKK4JBbkY1rUSN18vEBV6vGUZAV2QU5Odv1EBBYa33qALAnL3RcLmz9o9vmytd1eQSZAjDelalzrz4ZCLqcgw87fiNioTbdtCBoMWZBux7UmUX6oLfardN2t6NVQpO7kQIW20r2YXnqWy0743fsfzTqvfwZBdEJawH426FH7ZBbh5aB6qO05wZDZD" # The key changes through the time, check the app in facebook.developers

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
