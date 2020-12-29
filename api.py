from pyfacebook import Api
import json  # Use the json module to write the files

APP_ID = "432341101134225"
KEY_SECRET = "5f1a24aa9fc8ebd8f6e5cd26a1603ac3"  # The key changes through the time, check the app in facebook.developers
PAGE_ID = "103914631637231"
ACCESS_TOKEN = "EAAGJNkHBQZAEBAHHMFyy0jmnae2ZBq1RP0Uh02bGNL8fbaIlD3aET4OYODLlU8uhQWG0taCRYLOYtPZC8x44JfcjZAMwaoDTfGCQOZBLTdjbwDyVdmL09oInrRuZB5AFfPPmfZAtiBMp6LfXkOwEWtYmv4Hrz1M3eSbp5elD2NkqUjT5WXCEODY"  # The key changes through the time, check the app in facebook.developers

# TODO Declare the necessary functions to carry out the draft


def connection():
    api = ''
    try:
        api = Api(app_id=APP_ID, app_secret=KEY_SECRET, long_term_token=ACCESS_TOKEN)
    except ConnectionError as error:
        print(f'Problemas de conexion: {error}')
    except Exception as error:
        print(error)
    return api, True


def main():
    data, isConnected = connection()
    if isConnected:
        print(data.get_published_posts(page_id=PAGE_ID))


main()
