from logs import write_status_log, write_chat_bot, user_options, GET_NAME
import facebook
import os.path
from termcolor import cprint

USER_TOKEN = "EAAGJNkHBQZAEBALHnRf3grXqjMdGG8denwyen9hvbCAYHRtsUdb315ZBUa5QvtdN3XkkyIRi3J2WZCp5zuYdlVdYOPgmbMGUc84D6S7MAw3E6qvUKZCL7UPvFaeZAGN3U06G5sJBTleNlQuFSFR1wzVSJLfpc2SyWxPI9nRFnYFb7RLhOdTYHfNti2NZCHx5wZD"


# READ_POST = 0
# UPDATE_POST = 1
# GET_POST = 2


def get_albums(graph, caption, path):
    """
    
    :param graph:
    :param caption:
    :param path:
    :return:
    """
    # It needs the graph, a caption for the photo, and the path for said photo
    # It uploads it to an album which the user specifies
    counter = 1
    select = 0
    albums_id = []
    albums = graph.get_connections(id = 'me', connection_name = 'albums')
    info_list = albums['data']
    print("Your albums are: ")
    write_chat_bot("Your albums are: ")
    for info in info_list[0:5]:
        print(f"{counter} -", info["name"])
        counter += 1
        albums_id.append(info["id"])
        write_chat_bot(f"{counter} -", info["name"])
    
    while select > counter or select < 1:
        select = int(input("Select the album: "))
        write_chat_bot("Select the album: ")
    try:
        graph.put_photo(image = open(path, 'rb'), album_path = albums_id[select - 1] + "/photos", message = caption)
        cprint("The photo has been uploaded successfully!", 'green', attrs = ['bold'])
        write_chat_bot("The photo has been uploaded successfully!")
    except FileNotFoundError:
        write_status_log("The requested file cannot be found")
        print("The requested file cannot be found")
    except Exception as error:
        write_status_log(f"There was a problem opening the file, error: {error}")
        print(f"There was a problem opening the file, error: {error}")


def search_file() -> str or bool:
    """
    PRE: -
    POST: Searches for a photo in the user desktop. The file must be .jpg
    :return:
    """
    found_file = False
    path = ''
    name = user_options(GET_NAME)
    while not found_file:
        path = input("Enter the file path, the file must be .jpg: ")
        write_chat_bot("Enter the file path, the file must be .jpg: ")
        path = os.path.abspath(path)
        write_chat_bot(path, name)
        if os.path.exists(path):
            found_file = True
        else:
            cprint("The path doesnt exists, please enter a correct path \n", 'red', attrs = ['bold'])
            write_chat_bot("The path doesnt exists, please enter a correct path")
    return path


def upload_to_albums(graph) -> None:
    """
    PRE: It needs the graph and can't be null
    POST: It uploads it to an album which the user specifies
    :param graph:
    :return:
    """
    path = search_file()
    name = user_options(GET_NAME)
    if path:
        counter = 1
        select = 0
        albums_id = []
        albums = graph.get_connections(id = 'me', connection_name = 'albums')
        info_list = albums['data']
        print("Your albums are: ")
        write_chat_bot("Your albums are: ")
        for info in info_list[0:5]:
            print(f"{counter} -", info["name"])
            counter += 1
            albums_id.append(info["id"])
            write_chat_bot(f"{counter} -", info["name"])
        
        while select > counter or select < 1:
            select = int(input("Select the album: "))
            write_chat_bot("Select the album: ")
        
        caption = input("Caption: ")
        write_chat_bot("Caption: ")
        write_chat_bot(caption, name)
        try:
            graph.put_photo(image = open(path, 'rb'), album_path = albums_id[select - 1] + "/photos", message = caption)
            cprint("The photo has been uploaded successfully!", 'green', attrs = ['bold'])
            write_chat_bot("The photo has been uploaded successfully!")
        except FileNotFoundError:
            write_status_log("The requested file cannot be found")
            print("The requested file cannot be found")
        except Exception as error:
            write_status_log(f"There was a problem opening the file, error: {error}")
            print(f"There was a problem opening the file, error: {error}")


# TODO Refactorizar las funciones de posts y photos, son muy similares todas
def upload_photo(graph) -> None or Exception:
    """
    PRE: Needs the path of the picture and a caption and the parameter can't be null
    POST: It uploads it with a caption written by the user
    :param graph:
    :return:
    """
    path = search_file()
    caption = input("Caption: ")
    name = user_options(GET_NAME)
    write_chat_bot("Caption: ")
    write_chat_bot(caption, name)
    try:
        graph.put_photo(image = open(path, 'rb'), message = caption)
        cprint("The photo has been uploaded successfully!", 'green', attrs = ['bold'])
        write_chat_bot("The photo has been uploaded successfully!")
    except FileNotFoundError:
        write_status_log("The requested file cannot be found")
        print("The requested file cannot be found")
    except Exception as error:
        write_status_log(f"There was a problem opening the file, error: {error}")
        print(f"There was a problem opening the file, error: {error}")


def upload_post(graph) -> None or Exception:
    """
    
    :param graph:
    :return:
    """
    name = user_options(GET_NAME)
    user_message = input("What would you like to write?: ")
    write_chat_bot("What would you like to write?: ")
    write_chat_bot(user_message, name)
    try:
        graph.put_object(parent_object = 'me', connection_name = 'feed', message = user_message)
    except Exception as error:
        write_status_log('Failed', error)
        print(f"There was a problem uploading your post, error: {error}")
        raise Exception(error)


def like_post(graph):
    """
    PRE: The parameter can't be null
    :param graph:
    :return:
    """
    option = 0
    posts_id, counter = read_posts(graph)
    name = user_options(GET_NAME)
    
    response = input("Do you want to like a post?(Yes or No): ").lower()
    write_chat_bot("Do you want to like a post?(Yes or No): ")
    write_chat_bot(response, name)
    if response == "yes":
        while option > counter or option < 1:
            option = int(input("Select the post to like: "))
            write_chat_bot("Select the post to like: ")
            write_chat_bot(option, name)
        
        graph.put_like(object_id = posts_id[option - 1])


def follower_count(graph) -> None:
    """
    PRE: The parameter can't be null
    POST: Make an print of the number of followers of the page
    :param graph:
    :return: None
    """
    followers = graph.get_object(id = 'me', fields = 'followers_count')
    print(f"Number of followers: {str(followers['followers_count'])}")
    write_chat_bot(f"Number of followers: {str(followers['followers_count'])}")


def read_posts(graph) -> tuple:
    """
    PRE: The parameter can't be null
    :param graph:
    :return:
    """
    counter = 1
    posts_id = []
    posts = graph.get_connections(id = 'me', connection_name = 'visitor_posts')
    info_list = posts['data']
    print("The posts are: ")
    write_chat_bot("The posts are: ")
    for info in info_list:
        if 'message' in info:
            print(f"{counter}. " + info["created_time"][0:10] + ":" + info["message"])
            write_chat_bot(f"{counter}. " + info["created_time"][0:10] + ":" + info["message"])
            counter += 1
            posts_id.append(info["id"])
        elif 'story' in info:
            print(f"{counter}. " + info["created_time"][0:10] + ":" + info["story"])
            write_chat_bot(f"{counter}. " + info["created_time"][0:10] + ":" + info["story"])
            counter += 1
            posts_id.append(info["id"])
        elif 'story' or 'message' not in info:
            print(f"{counter}. " + info["created_time"][0:10])
            write_chat_bot(f"{counter}. " + info["created_time"][0:10])
    
    return posts_id, counter


def get_post_to_edit(graph) -> str or int:
    """
    PRE: The parameter can't be null
    POST: Fetch the ids of the last 5 posts and display them in some sort of menu
    :param graph:
    :return:
    """
    counter = 1
    option = 0
    posts_id = []
    name = user_options(GET_NAME)
    posts = graph.get_connections(id = 'me', connection_name = 'posts')
    info_list = posts['data']
    print("This are your last 5 posts: ")
    write_chat_bot("This are your last 5 posts: ")
    for info in info_list[0:5]:
        if 'message' in info:
            text = f"{counter}º -\t" + info["message"]
            print(text)
            write_chat_bot(text)
            counter += 1
            posts_id.append(info["id"])
    
    while option > counter or option < 1:
        option = int(input("Select one: "))
        write_chat_bot("Select one: ")
        write_chat_bot(option, name)
    
    return posts_id[option - 1]


def edit_post(graph) -> None:
    """
    PRE: The parameter can't be null
    POST: The user can edit or delete a post made by them
    :param graph:
    :return:
    """
    post = get_post_to_edit(graph)
    name = user_options(GET_NAME)

    option = input("Do you want to delete the post or edit?: ").lower()
    write_chat_bot("Do you want to delete the post or edit?: ")
    write_chat_bot(option, name)
    if option in ['delete', 'd', 'del', 'delete post', 'delete the post']:
        graph.delete_object(id = post)
    elif option in ['edit', 'e', 'ed', 'edit post', 'edit the post']:
        text = input("What would you like to post?: ").capitalize()
        write_chat_bot("What would you like to post?: ")
        write_chat_bot(text, name)
        graph.put_object(parent_object = post, connection_name = '', message = text)


# ------------ CONNECTION ---------------#

def connection_api(user_token = USER_TOKEN) -> object or Exception:
    """
    Returns the GraphApi and checks if there was any error while connecting to Facebook
    :return:
    """
    try:
        api = facebook.GraphAPI(access_token = user_token, version = "2.12")
    except ConnectionError as error:
        write_status_log(error, 'Connection error')
        raise ConnectionError(f'You dont have internet: {error}')
    except Exception as error:
        write_status_log(error, 'Failed')
        raise Exception(error)
    else:
        write_status_log('Successfully connected with Facebook the api')
        cprint('\nYou have successfully connected with the Facebook api!\n', 'green', attrs = ['bold'])
        write_chat_bot('You have successfully connected with the Facebook api!')
    
    return api
