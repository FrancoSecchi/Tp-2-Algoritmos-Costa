from logs import write_status_log, write_chat_bot, user_options, GET_NAME, get_credentials, remove_file
import facebook
import os.path
import json
from termcolor import cprint

USER_TOKEN = "EAAGJNkHBQZAEBALHnRf3grXqjMdGG8denwyen9hvbCAYHRtsUdb315ZBUa5QvtdN3XkkyIRi3J2WZCp5zuYdlVdYOPgmbMGUc84D6S7MAw3E6qvUKZCL7UPvFaeZAGN3U06G5sJBTleNlQuFSFR1wzVSJLfpc2SyWxPI9nRFnYFb7RLhOdTYHfNti2NZCHx5wZD"


# READ_POST = 0
# UPDATE_POST = 1
# GET_POST = 2


def upload_to_albums(graph) -> None:
    """
    PRE: It needs the graph and can't be null
    POST: It uploads it to an album which the user specifies
    :param graph:
    :return:
    """
    path = input("Please enter the path of your picture: ")
    name = user_options(GET_NAME)
    if path:
        counter = 1
        select = 0
        albums_id = []
        albums = graph.get_connections(id = 'me', connection_name = 'albums')
        info_list = albums['data']
        print("Your albums are: ")
        write_chat_bot("Your albums are: ")
        for info in info_list:
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

def upload_photo(graph) -> None or Exception:
    """
    PRE: Needs the path of the picture and a caption and the parameter can't be null
    POST: It uploads it with a caption written by the user
    :param graph:
    :return:
    """
    path = input("Please enter the path of your picture: ")
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
    POS:Uploads the photo with caption 
    :param graph:
    :return:
    """
    user_message = input("What would you like to write?: ")
    try:
        graph.put_object(parent_object = 'me', connection_name = 'feed', message = user_message)
    except Exception as error:
        write_status_log('Failed', error)
        print(f"There was a problem uploading your post, error: {error}")
        raise Exception(error)


def follower_count(graph) -> None:
    """
    PRE: The parameter can't be null
    POST: Make an print of the number of followers of the page
    :param graph:
    :return: None
    """
    followers = graph.get_object(id = 'me', fields = 'followers_count')
    print(f"Number of followers: {str(followers['followers_count'])}")


def post_related(graph,function,selected) -> None:
    """
    PRE: The function needs the purpose(function) of the call(Example: If it is for editing a post or liking a post) and 
    the selected posts(If they are made by the user or visitors posts on the page)
    POS: Executes the purpose specified
    :param graph:
    :return:
    """
    option = 0
    counter = 1
    posts_id = []
    try:
        posts = graph.get_connections(id = 'me', connection_name = selected)
        info_list = posts['data']
        print("The posts are: ")
        for info in info_list:
            if 'message' in info:
                print(f"{counter}. " + info["created_time"][0:10] + ":" + info["message"])
                counter += 1
                posts_id.append(info["id"])
            elif 'story' in info:
                print(f"{counter}. " + info["created_time"][0:10] + ":" + info["story"])
                counter += 1
                posts_id.append(info["id"])
            elif 'story' or 'message' not in info:
                print(f"{counter}. " + info["created_time"][0:10])

        while option > counter or option < 1:
                option = int(input("Select one: "))
            
        selection = posts_id[option - 1]

        if function == "like":
            graph.put_like(object_id = selection)

        elif function == "comment":
            text = input("What would you like to comment: ").capitalize()
            graph.put_comment(object_id= selection, message=text)

        elif function == "delete":
            graph.delete_object(id = selection)

        elif function == "edit":
            text = input("What would you like to change?: ").capitalize()
            graph.put_object(parent_object = selection, connection_name = '', message = text) 
    
    except Exception as error:
        write_status_log('Failed', error)
        print(f"There was a problem with the operation : {error}")
        raise Exception(error)           


# ------------ CONNECTION ---------------#

def connection_api(**user_token) -> object or Exception:
    """
    Returns the GraphApi and checks if there was any error while connecting to Facebook
    :return:
    """
    if "token" not in user_token.keys():
        credentials = get_credentials()
        page_token = credentials['facebook']['token']
    else:
        page_token = user_token["token"]    
    try:
        api = facebook.GraphAPI(access_token = page_token, version = "2.12")
    except ConnectionError as error:
        write_status_log(error, 'Connection error')
        raise ConnectionError(f'You dont have internet: {error}')
    except Exception as error:
        write_status_log(error, 'Failed')
        raise Exception(error)
    else:
        write_status_log('Successfully connected with Facebook the api')
        cprint('\nYou have successfully connected with the Facebook api!\n', 'green', attrs = ['bold'])
    
    return api

