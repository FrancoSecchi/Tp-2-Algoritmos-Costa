from logs import get_credentials
import facebook
from termcolor import cprint


def print_write_chatbot(text):
    print(text)
    write_chat_bot(text)


def cprint_write_chatbot(text, color, attrs):
    cprint(text, color, attrs)
    write_chat_bot(text)


def input_write_chatbot(text):
    input(text)
    write_chat_bot(text)


def show_albums(albums_id):
    albums = facebook_api.get_connections(id = 'me', connection_name = 'albums')
    info_list = albums['data']
    print_write_chatbot("Your albums are: ")
    for count, info in enumerate(info_list, start):
        print(count, info["name"])
        albums_id.append(info["id"])


def validate_select(select, albums_id):
    while select in range(len(albums_id)):
        select = int(input_write_chatbot("Select the album: "))


def upload_to_albums(facebook_api) -> None or Exception:
    """
    PRE: It needs the facebook_api and can't be null
    POST: It uploads it to an album which the user specifies
    """
    path = input_write_chatbot("Please enter the path of your picture: ")
    username = get_username()
    if path:
        albums_id = []
        show_albums(albums_id)
        select = int(input_write_chatbot("Select the album: "))
        validate_select(select, albums_id)
        caption = input_write_chatbot("Caption: ")
        try:
            facebook_api.put_photo(image = open(path, 'rb'), album_path = albums_id[select - 1] + "/photos", message = caption)
            cprint_write_chatbot("The photo has been uploaded successfully!", 'green', attrs = ['bold'])
        except FileNotFoundError:
            write_status_log("The requested file cannot be found", "FileNotFoundError")
            print("The requested file cannot be found")
        except Exception as error:
            write_status_log(f"There was a problem opening the file, error: {error}", "Exception")
            print(f"There was a problem opening the file, error: {error}")


def upload_photo(facebook_api) -> None or Exception:
    """
    PRE: Needs the path of the picture and a caption and the parameter can't be null
    POST: It uploads it with a caption written by the user
    """
    path = input_write_chatbot("Please enter the path of your picture: ")
    caption = input_write_chatbot("Caption: ")
    username = get_username()
    try:
        facebook_api.put_photo(image = open(path, 'rb'), message = caption)
        cprint_write_chatbot("The photo has been uploaded successfully!", 'green', attrs = ['bold'])
    except FileNotFoundError:
        write_status_log("The requested file cannot be found", 'FileNotFoundError')
        print("The requested file cannot be found")
    except Exception as error:
        write_status_log(f"There was a problem opening the file, error: {error}", 'Exception')
        return print("Error")


def upload_post(facebook_api) -> None or Exception:
    """
    PRE: The facebook_api cant be null
    POST: Updates a post chosen by the user
    """
    username = get_username()
    user_message = input_write_chatbot("What would you like to write?: ")
    try:
        facebook_api.put_object(parent_object = 'me', connection_name = 'feed', message = user_message)
        cprint("Posting has been updated successfully!\n", 'green', attrs = ['bold'])
    except Exception as error:
        write_status_log(error, 'Exception')
        return print("Error")


def follower_count(facebook_api) -> None:
    """
    PRE: The parameter can't be null
    POST: Make an print of the number of followers of the page
    """
    followers = facebook_api.get_object(id = 'me', fields = 'followers_count')
    print_write_chatbot(f"Number of followers: {str(followers['followers_count'])}\n")


def if_text_in_info(text, info, post_id, count):
    """
    PRE: The parameter can't be null
    POST: Make an print of the number of followers of the page
    """
    if text in info:
        print_write_chatbot(count, info["created_time"][0:10] + ":" + info[text])
        posts_id.append(info["id"])


def like():
    """
    PRE: action == "like"
    POST: likes the selection and prints the success of the action
    """
    facebook_api.put_like(object_id = selection)
    cprint_write_chatbot("The post has been liked successfully!\n", 'green', attrs = ['bold'])


def comment():
    """
    PRE: action == "comment"
    POST: comment the selection and prints the success of the action
    """
    text = input_write_chatbot("What would you like to comment: ").capitalize()
    facebook_api.put_comment(object_id = selection, message = text)
    cprint_write_chatbot("It has been successfully commented!\n", 'green', attrs = ['bold'])


def delete_post():
    """
    PRE: action == "delete"
    POST: deletes the selection and prints the success of the action
    """
    facebook_api.delete_object(id = selection)
    cprint_write_chatbot("The post has been successfully removed!\n", 'green', attrs = ['bold'])


def edit_post():
    """
    PRE: action == "edit"
    POST: edits the selection and prints the success of the action
    """
    text = input_write_chatbot("What would you like to change?: ").capitalize()
    facebook_api.put_object(parent_object = selection, connection_name = '', message = text)
    cprint_write_chatbot("Posting has been updated successfully!\n", 'green', attrs = ['bold'])


def validate_option(option, posts_id):
    while option in range(len(posts_id)):
        option = int(input_write_chatbot("Select one: "))


def post_related(facebook_api, action, selected) -> None:
    """
    PRE: The function needs the purpose(action) of the call(Example: If it is for editing a post or liking a post) and
    the selected posts(If they are made by the user or visitors posts on the page)
    POST: The posts of the page are shown and depending on the action, it will be edited / liked/ deleted / commented
    """
    posts_id = []
    username = get_username()
    try:
        posts = facebook_api.get_connections(id = 'me', connection_name = selected)
        info_list = posts['data']
        cprint_write_chatbot("The posts are: ")
        for count, info in enumerate(info_list, start = 1):
            if_text_in_info("message", info, post_id, count)
            if_text_in_info("story", info, post_id, count)
            print_write_chatbot(count, info["created_time"][0:10])
            posts_id.append(info["id"])
        option = int(input_write_chatbot("Select one: "))
        validate_option(option, posts_id)
        selection = posts_id[option - 1]
        
        if action == "like":
            like()
        elif action == "comment":
            comment()
        elif action == "delete":
            delete_post()
        elif action == "edit":
            edit_post()

    except Exception as error:
        write_status_log(error, 'Exception')
        return print("Error")


# ------------ CONNECTION ---------------#


def connection_api(user_credentials: dict = {}) -> object:
    """
    PRE: The parameters can be null
    PRE: If the user does not enter their credentials, those of crux are used.
         Returns the facebook_apiApi and checks if there was any error while connecting to Facebook
    """
    if "token" not in user_credentials.keys():
        credentials = get_credentials()
        page_token = credentials['facebook']['token']
    else:
        page_token = user_credentials["token"]
    try:
        api = facebook.GraphAPI(access_token = page_token, version = "2.12")
    except ConnectionError as error:
        write_status_log(error, 'ConnectionError')
        return print(f'You dont have internet: {error}')
    except Exception as error:
        write_status_log(error, 'Exception')
        return print("Error")
    else:
        write_status_log('Successfully connected with Facebook the api')
        cprint('\nYou have successfully connected with the Facebook api!\n', 'green', attrs = ['bold'])
    
    return api
