from logs import write_status_log
import facebook
import os.path

USER_TOKEN = "EAAGJNkHBQZAEBAO73ZAGv7kK71OPd3a7TSmF17OxluZBkOLKgQ8GZAvPm4J5PWUzwKdZCHrSQE2SuNmFl2lTgPcSZCY5hPbV8ZBfPElL1hkIJC2Ra7tucOf3m2Y0Qo90X9ZAfYcZBfDOfaf46CbmXQ0usEmkmg3yF8Ywr134bVeMlpJ1tJm164AmNghli50YJULkZD"
READ_POST_OPTION = 0
UPDATE_POST_OPTION = 1
GET_POST_OPTION = 2


def connection_api(user_token=USER_TOKEN) -> object or Exception:
    """
    Returns the GraphApi and checks if there was any error while connecting to Facebook
    :return:
    """
    try:
        api = facebook.GraphAPI(access_token=user_token, version="2.12")
    except ConnectionError as error:
        write_status_log(error, 'Connection error')
        raise ConnectionError(f'You dont have internet: {error}')
    except Exception as error:
        write_status_log(error, 'Failed')
        raise Exception(error)
    else:
        write_status_log('Successfully connected with the api')
        print('You have successfully connected with the Facebook api!')

    return api


def search_file() -> str or bool:
    """
    PRE: -
    POST: Searches for a photo in the user desktop. The file must be .jpg
    :return:
    """
    found_file = False
    path = ''
    while not found_file:
        path = input("Enter the file path: ")
        if os.path.exists(path):
            found_file = True
        else:
            print("The path doesnt exists, please enter a correct path \n")
    return path


def upload_to_albums(graph) -> None:
    """
    PRE: It needs the graph and can't be null
    POST: It uploads it to an album which the user specifies
    :param graph:
    :return:
    """
    path = search_file()
    if path:
        counter = 1
        select = 0
        albums_id = []
        albums = graph.get_connections(id='me', connection_name='albums')
        info_list = albums['data']
        print("Sus albums son: ")
        for info in info_list[0:5]:
            print(f"{counter} -", info["name"])
            counter += 1
            albums_id.append(info["id"])

        while select > counter or select < 1:
            select = int(input("Seleccione el album: "))

        caption = input("Caption: ")
        graph.put_photo(image=open(path, 'rb'), album_path=albums_id[select - 1] + "/photos", message=caption)


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
    try:
        graph.put_photo(image=open(path, 'rb'), message=caption)
    except FileNotFoundError:
        print("El archivo solicitado no se encuentra")
    except Exception as error:
        print(f"Hubo un problema abriendo el archivo, error: {error}")


def upload_post(graph) -> None or Exception:
    user_message = input("What would you like to write?: ")
    try:
        graph.put_object(parent_object='me', connection_name='feed', message=user_message)
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
    counter = 1
    option = 0
    posts_id = []
    posts = graph.get_connections(id='me', connection_name='posts')
    info_list = posts['data']
    print("Your posts are: ")
    for info in info_list:
        if 'message' in info:
            print(f"{counter} -", info["created_time"][0:10] + ":" + info["message"])
            counter += 1
            posts_id.append(info["id"])
        elif 'story' in info:
            print(f"{counter} -", info["created_time"][0:10] + ":" + info["story"])
            counter += 1
            posts_id.append(info["id"])
        elif 'story' or 'message' not in info:
            print(f"{counter} -", info["created_time"][0:10])

    while option > counter or option < 1:
        option = int(input("Seleccione el post a likear: "))

    graph.put_like(object_id=posts_id[option - 1])


def follower_count(graph) -> None:
    """
    PRE: The parameter can't be null
    POST: Make an print of the number of followers of the page
    :param graph:
    :return: None
    """
    followers = graph.get_object(id='me', fields='followers_count')
    print(f"Number of followers: {str(followers['followers_count'])}")


def read_posts(graph) -> None:
    """
    PRE: The parameter can't be null
    :param graph:
    :return:
    """
    counter = 1
    posts_id = []
    posts = graph.get_connections(id='me', connection_name='posts')
    info_list = posts['data']
    print("The posts are: ")
    for info in info_list:
        if 'message' in info:
            print(info["created_time"][0:10] + ":" + info["message"])
            counter += 1
            posts_id.append(info["id"])
        elif 'story' in info:
            print(info["created_time"][0:10] + ":" + info["story"])
            counter += 1
            posts_id.append(info["id"])
        elif 'story' or 'message' not in info:
            print(info["created_time"][0:10])


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
    posts = graph.get_connections(id='me', connection_name='posts')
    info_list = posts['data']
    print("This are your last 5 posts: ")
    for info in info_list[0:5]:
        if 'message' in info:
            print(f"{counter} -", info["message"])
            counter += 1
            posts_id.append(info["id"])

    while option > counter or option < 1:
        option = int(input("Select one: "))

    return posts_id[option - 1]


def edit_post(graph) -> None:
    """
    PRE: The parameter can't be null
    POST: The user can edit or delete a post made by them
    :param graph:
    :return:
    """
    post = get_post_to_edit(graph)

    option = input("Do you want to delete the post or edit?: ").lower()

    if option in ['delete', 'd', 'del', 'delete post', 'delete the post']:
        graph.delete_object(id=post)
    elif option in ['edit', 'e', 'ed', 'edit post', 'edit the post']:
        text = input("What would you like to post?: ").capitalize()
        graph.put_object(parent_object=post, connection_name='', message=text)
