from logs import (write_log, STATUS_FILE, get_credentials,
                  print_write_chatbot, input_user_chat)
import facebook
from termcolor import cprint  


def show_albums(albums_id: list):
    """ 
    Prints a list of albums of the user
    
    Arguments:
        albums_id (list): Contains the albums of the user
    
    Returns:
        None
        
    """
    albums = facebook_api.get_connections(id = 'me', connection_name = 'albums')
    info_list = albums['data']
    print_write_chatbot("Your albums are: ")
    for count, info in enumerate(info_list, start):
        print(count, info["name"])
        albums_id.append(info["id"])
    
def validate(number, list_):
    """
    Validates the input put by the user
    
    Arguments:
        number (int): Number of the album selected
        list_ (list): Contains the albums of the user
    
    Returns:
        int - The value of the input given by the user
    """
    while number in range(len(list_)):
        number = int(input_user_chat("re select: "))


def upload_to_albums(facebook_api: facebook.GraphAPI) -> None:
    """
    Uploads a picture from the user to the album the user must select
    
    Arguments:
        facebook_api (object) : facebook api graph
    
    Returns:
        None
    """

    path = input_user_chat("Please enter the path of your picture: ")
    if path:
        albums_id = []
        show_albums(albums_id)
        select = int(input_user_chat("Select the album: "))
        validate_select(select, albums_id)
        caption = input_user_chat("Caption: ")
        try:
            facebook_api.put_photo(image = open(path, 'rb'), album_path = albums_id[select - 1] + "/photos", message = caption)
            print_write_chatbot("The photo has been uploaded successfully!", 'green', attrs = ['bold'])
        except FileNotFoundError:
            write_log("The requested file cannot be found", "FileNotFoundError")
            print("The requested file cannot be found")
        except Exception as error:
            write_log(f"There was a problem opening the file, error: {error}", "Exception")
            print(f"There was a problem opening the file, error: {error}")


def upload_photo(facebook_api: facebook.GraphAPI) -> None or Exception:
    """
    Asks the user the path of the photo and the caption the user wants to upload, and uploads the photo and the caption 
    
    Arguments:
        facebook_api (object) : facebook api graphThe facebook api
    
    Returns:
        None
    """
    path = input_user_chat("Please enter the path of your picture: ")
    caption = input_user_chat("Caption: ")
    name = get_username()
    try:
        facebook_api.put_photo(image = open(path, 'rb'), message = caption)
        print_write_chatbot("The photo has been uploaded successfully!", 'green', attrs = ['bold'])
    except FileNotFoundError:
        write_log("The requested file cannot be found", 'FileNotFoundError')
        print("The requested file cannot be found")
    except Exception as error:
        write_log(f"There was a problem opening the file, error: {error}", 'Exception')
        print("Error")

def upload_post(facebook_api: facebook.GraphAPI) -> None or Exception:
    """
    Uploads the post written by the user and prints the success of the action if there are no errors 
    
    Arguments:
        facebook_api (object) : facebook api graph
    
    Returns:
        None
    """
    name = get_username()
    user_message = input_user_chat("What would you like to write?: ")
    try:
        facebook_api.put_object(parent_object = 'me', connection_name = 'feed', message = user_message)
        cprint("Posting has been updated successfully!\n", 'green', attrs = ['bold'])
    except Exception as error:
        write_log(error, 'Exception')
        print("Error")

def follower_count(facebook_api: facebook.GraphAPI) -> None:
    """
    Prints the count of followers of the page
    
    Arguments:
        facebook_api (object) : facebook api graph
    
    Returns:
        None
    """

    followers = facebook_api.get_object(id = 'me', fields = 'followers_count')
    print_write_chatbot(f"Number of followers: {str(followers['followers_count'])}\n")


def if_text_in_info(text, info, post_id, count):
    """
    Prints the number, the created time and the contend of the post,
    and appends its id in the post_id list
    
    Arguments:
        text (str) : Type of data in the info
        info (list) : Data of the posts in the graph
        posts_id (list) : List of the posts of the page
        count (int) : The number of the post
        
    Returns:
        None
    """
    if text in info:
        print_write_chatbot(count, info["created_time"][0:10] + ":" + info[text])
        posts_id.append(info["id"])


def like(facebook_api: facebook.GraphAPI, selection: int):

    """
    Likes the selection and prints the success of the action
    
    Arguments:
        facebook_api (object) : facebook api graph
        selection (int) : The number of the post the user selected
    
    Returns:
        object - (facebook_api)
    """
    facebook_api.put_like(object_id = selection)
    print_write_chatbot("The post has been liked successfully!\n", 'green', attrs = ['bold'])
    
def comment(facebook_api: facebook.GraphAPI, selection: int):
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
    print_write_chatbot("It has been successfully commented!\n", 'green', attrs = ['bold'])

def delete_post(facebook_api: facebook.GraphAPI, selection: str):
    """
    Deletes the selected post
    
    Arguments:
        facebook_api (object) : facebook api graph
        selection (int) : The number of the post the user selected
        
    Returns:
        object - (facebook_api)
    """
    facebook_api.delete_object(id = selection)
    print_write_chatbot("The post has been successfully removed!\n", 'green', attrs = ['bold'])

def edit_post(facebook_api: facebook.GraphAPI, selection: int):
    """
    Edits the selection and prints the success of the action 
    
    Arguments:
        facebook_api (object) : facebook api graph
        selection (int) : The number of the post the user selected 
        
    Returns:
        object - (facebook_api)
    """
    text = input_user_chat("What would you like to change?: ").capitalize()
    facebook_api.put_object(parent_object = selection, connection_name = '', message = text)
    print_write_chatbot("Posting has been updated successfully!\n", 'green', attrs = ['bold'])


def post_related(facebook_api, action, selected) -> None:
    """
    The posts of the page are shown and depending on the action, it will be edited / liked/ deleted / commented
    
    Arguments:
        facebook_api (object) : facebook api graph
        action (str) : The action the user wants to do
        selected (str) : The connection name the user selected
    
    Returns: None
    """
    posts_id = []
    name = get_username()
    try:
        posts = facebook_api.get_connections(id = 'me', connection_name = selected)
        info_list = posts['data']
        print_write_chatbot("The posts are: ")
        for count, info in enumerate(info_list, start=1):
            if_text_in_info("message", info, posts_id, count)
            if_text_in_info("story", info, posts_id, count)

        option = int(input_user_chat("Select one: "))
        validate(option, posts_id)
        selection = posts_id[option - 1]
        
        if action == "like":
            like(facebook_api, selection)
        elif action == "comment":
            comment(facebook_api, selection)
        elif action == "delete":
            delete_post(facebook_api, selection)
        elif action == "edit":
            edit_post(facebook_api, selection)
    
    except Exception as error:
        write_log(error, 'Exception')
        print("Error")


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
    except ConnectionError as error:
        write_log(STATUS_FILE, str(error), 'ConnectionError')
        print(f'You dont have internet: {error}')
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'ConnectionError')
        print ("Error")
    else:
        write_log(STATUS_FILE,'Successfully connected with Facebook the api', 'Crux')
        print_write_chatbot('You have successfully connected with the Facebook api!\n', color = 'green', attrs_color = ['bold'])
    
    return facebook_api
