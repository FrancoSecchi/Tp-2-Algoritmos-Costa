import os

from logs import (write_log, STATUS_FILE, get_credentials,
                  print_write_chatbot, input_user_chat)
import facebook
from termcolor import cprint


def show_albums(facebook_api: facebook.GraphAPI, albums_id: list) -> None:
    """ 
    Prints a list of albums of the user
    
    Arguments:
        facebook_api (facebook.GraphAPI)
        albums_id (list): Contains the albums of the user
    
        
    """
    albums = facebook_api.get_connections(id = 'me', connection_name = 'albums')
    info_list = albums['data']
    print_write_chatbot("Your albums are: ")
    for count, info in enumerate(info_list, 1):
        print(count, info["name"])
        albums_id.append(info["id"])


def validate_number(number: int, list_: list) -> int:
    """
    Validates the input put by the user
    
    Arguments:
        number (int): Number of the list selected
        list_ (list): Contains the list of the user
    
    Returns:
        int - The value of the input given by the user
    """
    while number not in range(len(list_)):
        number = int(input_user_chat("re select: "))
    return number


def upload_to_albums(facebook_api: facebook.GraphAPI) -> None:
    """
    Uploads a picture from the user to the album the user must select
    
    Arguments:
        facebook_api (object) : facebook api graph
  
    """
    
    path = input_user_chat("Please enter the path of your picture: ")
    if path:
        albums_id = []
        show_albums(facebook_api, albums_id)
        select = int(input_user_chat("Select the album: "))
        select = validate(select, albums_id)
        caption = input_user_chat("Caption: ")
        try:
            facebook_api.put_photo(image = open(path, 'rb'), album_path = albums_id[select - 1] + "/photos",
                                   message = caption)
            print_write_chatbot("The photo has been uploaded successfully!", color = "green",
                                attrs_color = ["bold"])
        except Exception as error:
            write_log(STATUS_FILE, f"There was a problem opening the file, error: {error}", "Exception")
            print_write_chatbot(f"There was a problem opening the file, error: {error}", color = "red",
                                attrs_color = ["bold"])


def search_file() -> str:
    """
    A file is searched and validated based on an absolute path
    
    Returns:
        str - Absoulte path of file
    
    """
    found_file = False
    path = ''
    while not found_file:
        path = os.path.abspath(input_user_chat("Enter the file path, the file must be .jpg: "))
        if os.path.exists(path):
            found_file = True
        else:
            print_write_chatbot(f"The path doesnt exists, please enter a correct path \n", color = "red",
                                attrs_color = ["bold"])
    return path


def upload_photo(facebook_api: facebook.GraphAPI) -> None or Exception:
    """
    Asks the user the path of the photo and the caption
    the user wants to upload, and uploads the photo and the caption
    
    Arguments:
        facebook_api (object) : facebook api graphThe facebook api
    
    """
    path = search_file()
    caption = input_user_chat("Caption: ")
    try:
        facebook_api.put_photo(image = open(path, 'rb'), message = caption)
        print_write_chatbot("The photo has been uploaded successfully!", color = 'green', attrs_color = ["bold"])
    except Exception as error:
        write_log(STATUS_FILE, f"There was a problem uploading the file, error: {error}", 'Exception')
        print_write_chatbot(f"There was a problem uploading the file, error: {error}", color = "red",
                            attrs_color = ["bold"])


def upload_post(facebook_api: facebook.GraphAPI) -> None:
    """
    Uploads the post written by the user and prints the success of the action if there are no errors 
    
    Arguments:
        facebook_api (object) : facebook api graph
    
    """
    user_message = input_user_chat("What would you like to write?: ")
    try:
        facebook_api.put_object(parent_object = 'me', connection_name = 'feed', message = user_message)
        print_write_chatbot("Posting has been updated successfully!\n", color = 'green', attrs_color = ["bold"])
    except Exception as err:
        write_log(STATUS_FILE, str(err), 'Exception')
        print_write_chatbot(f"Error to upload a post {err}", color = "red", attrs_color = ['bold'])


def follower_count(facebook_api: facebook.GraphAPI) -> None:
    """
    Prints the count of followers of the page
    
    Arguments:
        facebook_api (object) : facebook api graph
 
    """
    
    followers = facebook_api.get_object(id = 'me', fields = 'followers_count')
    print_write_chatbot(f"Number of followers: {str(followers['followers_count'])}\n")


def like(facebook_api: facebook.GraphAPI, selection: int) -> None:
    """
    Likes the selection and prints the success of the action
    
    Arguments:
        facebook_api (object) : facebook api graph
        selection (int) : The number of the post the user selected
    
    Returns:
        object - (facebook_api)
    """
    facebook_api.put_like(object_id = selection)
    print_write_chatbot("The post has been liked successfully!\n", color = 'green', attrs_color = ["bold"])


def comment(facebook_api: facebook.GraphAPI, selection: int) -> None:
    """
    Ask what would you like to comment, comments your response and prints the success of the action
    
    Arguments:
        facebook_api (object) : facebook api graph
        selection (int) : The number of the post the user selected
        
    Returns:
        object - (facebook_api)
    """
    text = input_user_chat("What would you like to comment: ").capitalize()
    facebook_api.put_comment(object_id = selection, message = text)
    print_write_chatbot("It has been successfully commented!\n", color = 'green', attrs_color = ["bold"])


def delete_post(facebook_api: facebook.GraphAPI, selection: str) -> None:
    """
    Deletes the selected post
    
    Arguments:
        facebook_api (object) : facebook api graph
        selection (int) : The number of the post the user selected
        
    Returns:
        object - (facebook_api)
    """
    facebook_api.delete_object(id = selection)
    print_write_chatbot("The post has been successfully removed!\n", color = 'green', attrs_color = ["bold"])


def edit_post(facebook_api: facebook.GraphAPI, selection: int, message: str) -> None:
    """
    Edits the selection and prints the success of the action 
    
    Arguments:
        facebook_api (object) : facebook api graph
        selection (int) : The number of the post the user selected 
        message (str) :  New message of post
        
    Returns:
        object - (facebook_api)
    """
    facebook_api.put_object(parent_object = selection, connection_name = '', message = message)
    print_write_chatbot("Posting has been updated successfully!\n", color = 'green', attrs_color = ["bold"])


def if_text_in_info(info: dict, posts_id: list, count: int):
    """
    Prints the number, the created time and the contend of the post,
    and appends its id in the post_id list

    Arguments:
        info (dict) : Data of the posts in the graph
        posts_id (list) : List of the posts of the page
        count (int) : The number of the post

    """
    
    if "message" in info:
        text_description = f": {info['message']}"
    elif "story" in info:
        text_description = f": {info['story']}"
    else:
        text_description = ''
    
    print_write_chatbot(f"{count}, {info['created_time'][0:10]} {text_description}")
    posts_id.append(info["id"])


def post_related(facebook_api: facebook.GraphAPI, action, selected) -> None:
    """
    The posts of the page are shown and depending on the action, it will be edited / liked/ deleted / commented
    
    Arguments:
        facebook_api (object) : facebook api graph
        action (str) : The action the user wants to do
        selected (str) : The connection name the user selected
    
    """
    posts_id = []
    selection = 0
    try:
        posts = facebook_api.get_connections(id = 'me', connection_name = selected)
        info_list = posts['data']
        print_write_chatbot("The posts are: ")
        for count, info in enumerate(info_list, start = 1):
            if_text_in_info(info, posts_id, count)
        
        if action != "read":
            option = int(input_user_chat("Select one: "))
            option = validate(option, posts_id)
            selection = posts_id[option - 1]
        
        if action == "like":
            like(facebook_api, selection)
        elif action == "comment":
            comment(facebook_api, selection)
        elif action == "delete":
            delete_post(facebook_api, selection)
        elif action == "edit":
            text = input_user_chat("Enter the new caption: ").capitalize()
            edit_post(facebook_api, selection, message = text)
    
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Exception')
        print_write_chatbot(f"Error {error}", color = "red", attrs_color = ["bold"])


# ------------ CONNECTION ---------------#


def connection_api(user_credentials: dict = {}) -> object:
    """
    If the user does not enter their credentials, those of crux are used.
    Returns the facebook Api and checks if there was any error while connecting to Facebook
    
    Arguments:
        user_credentials (str): users token
    
    Returns:
        object - (facebook_api)
    """
    facebook_api = ''
    if not user_credentials:
        credentials = get_credentials()
        page_token = credentials['facebook']['token']
    else:
        page_token = user_credentials["token"]
    
    try:
        facebook_api = facebook.GraphAPI(access_token = page_token, version = "2.12")
    except Exception as err:
        write_log(STATUS_FILE, str(err), 'ConnectionError')
        print("Error")
    else:
        write_log(STATUS_FILE, 'Successfully connected with Facebook the api', 'GraphAPI')
        print_write_chatbot('You have successfully connected with the Facebook api!\n', color = 'green',
                            attrs_color = ["bold"])
    
    return facebook_api
