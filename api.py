import facebook
import os
from instabot import Bot
from logs import write_status_log

USER_TOKEN = "EAAGJNkHBQZAEBAPaFOXzg1ZBiEiKcmHJlKEOQCygEwsH20hhYlqc9mmPZCEv3pbfxIHR7qxEykjKniz38wZAZASrxZCDiFKu4ICZBvWjEJqB22N2BRc2ClIrlJ2gMXuYn63SdYsBsco1K17ITTgcuRL20esIzhehdh91MZBXsuFDL0AYff9kKrFBQ2uHuSoow9nfVpjSgnQzfAZDZD"
READ_POST_OPTION = 0
UPDATE_POST_OPTION = 1
GET_POST_OPTION = 2


def connectionApi(user_token=USER_TOKEN) -> tuple or Exception:
    """
    Returns the GraphApi and checks if there was any error while connecting to Facebook
    :return:
    """
    api = ''
    try:
        api = facebook.GraphAPI(access_token=user_token, version="2.12")
    except ConnectionError as error:
        write_status_log(503, error)
        print(f'You dont have internet: {error}')
    except Exception as error:
        write_status_log(500, error)
        print(error)
    write_status_log(200, 'You have successfully connected with the api')
    print('You have successfully connected with the Facebook api')
    return api, True


def search_file() -> str:
    """
    Searchs for a photo in the user desktop. The file must be .jpg
    :return:
    """
    name = input("Ingrese el nombre del archivo: ")
    path = ''
    for root, dirs, files in os.walk(os.path.join(os.environ["HOMEPATH"], "Desktop")):
        for file in files:
            if file.endswith(name + ".jpg"):
                path = "C:" + root + f"\{str(file)}"
    return path


def upload_to_albums(graph, caption, path) -> None:
    """
    PRE: It needs the graph, a caption for the photo, and the path for said photo
    POST: It uploads it to an album which the user specifies
    :param graph:
    :param caption:
    :param path:
    :return:
    """
    path = search_file()
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

    graph.put_photo(image=open(path, 'rb'), album_path=albums_id[select - 1] + "/photos", message=caption)


# TODO Refactorizar las funciones de posts y photos, son muy similares todas
def upload_photo(graph, caption) -> None or Exception:
    """
    PRE: Needs the path of the picture and a caption
    POST: It uploads it with a caption written by the user
    :param graph:
    :param caption:
    :return:
    """
    path = search_file()
    try:
        graph.put_photo(image=open(path, 'rb'), message=caption)
    except FileNotFoundError:
        print("El archivo solicitado no se encuentra")
    except Exception as error:
        print(f"Hubo un problema abriendo el archivo, error: {error}")


def upload_post(graph) -> None or Exception:
    user_message = input("Que desea escribir?: ").capitalize()
    try:
        graph.put_object(parent_object='me', connection_name='feed', message=user_message)
    except Exception as error:
        write_status_log('Failed', error)
        print(f"Hubo un problema subiendo su post, error: {error}")


def like_post(graph):
    """

    :param graph:
    :return:
    """
    counter = 1
    option = 0
    posts_id = []
    posts = graph.get_connections(id='me', connection_name='posts')
    info_list = posts['data']
    print("Sus posts son: ")
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


def read_posts(graph) -> None:
    """

    :param graph:
    :return:
    """
    counter = 1
    posts_id = []
    posts = graph.get_connections(id='me', connection_name='posts')
    info_list = posts['data']
    print("Los posts son: ")
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
    POST: Fetch the ids of the last 5 posts and display them in some sort of menu
    :param graph:
    :return:
    """
    counter = 1
    option = 0
    posts_id = []
    posts = graph.get_connections(id='me', connection_name='posts')
    info_list = posts['data']
    print("Sus posts son: ")
    for info in info_list[0:5]:
        if 'message' in info:
            print(f"{counter} -", info["message"])
            counter += 1
            posts_id.append(info["id"])

    while option > counter or option < 1:
        option = int(input("Seleccione el post a editar: "))

    return posts_id[option - 1]


def edit_post(graph) -> None:
    """
    The user can edit or delete a post made by them
    :param graph:
    :return:
    """
    post = get_post_to_edit(graph)

    option = input("Do you want to delete the post or edit?: ").lower()

    if option in ['delete', 'd', 'del', 'delete post']:
        graph.delete_object(id=post)
    elif option in ['edit', 'e', 'ed', 'edit post']:
        text = input("Que desea escribir: ").capitalize()
        graph.put_object(parent_object=post, connection_name='', message=text)


# <======= INSTAGRAM =========>

def connectionInstagram(username='crux.bot', password='crux123'):
    """

    :param username:
    :param password:
    :return:
    """
    instaBot = Bot()
    try:
        instaBot.login(username=username, password=password)
    except ConnectionError as error:
        write_status_log(503, error)
        print(f'You dont have internet: {error}')
    except Exception as error:
        write_status_log(500, error)
        print(error)
    write_status_log(200, 'You have successfully connected with the Instagram bot')
    print('You have successfully connected with the Instagram bot')

    return instaBot, True


def search_users(bot) -> None:
    """

    :param bot:
    :return:
    """
    query = input("Who do you want to search? ")
    bot.search_users(query=query)
    json_data = bot.last_json
    counter = 1
    if json_data['num_results'] > 0:
        print("The users found are \n")
        for user in json_data['users']:
            full_data = ''
            full_data += f"{counter}) {user['username']} - {'Its a private profile' if user['is_private'] else 'Its a public profile'}"
            if 'social_context' in user.keys():
                full_data += f" - someone you know follows this account: {user['social_context']}"
            print(full_data, '\n')
            counter += 1

    else:
        print("")


def follow_actions(bot, username, type_follow='follow') -> bool or Exception:
    """

    :param type_follow:
    :param bot:
    :param username:
    :return:
    """
    try:
        user_id = bot.get_user_id_from_username(username)
        if type_follow == 'follow':
            return True if bot.follow(user_id=user_id) else False
        else:
            return True if bot.unfollow(user_id=user_id) else False
    except Exception as error:
        write_status_log(error, 500)
        print(error)
