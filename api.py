import facebook
from logs import writeStatusLog
import os

USER_TOKEN = "EAAGJNkHBQZAEBAPaFOXzg1ZBiEiKcmHJlKEOQCygEwsH20hhYlqc9mmPZCEv3pbfxIHR7qxEykjKniz38wZAZASrxZCDiFKu4ICZBvWjEJqB22N2BRc2ClIrlJ2gMXuYn63SdYsBsco1K17ITTgcuRL20esIzhehdh91MZBXsuFDL0AYff9kKrFBQ2uHuSoow9nfVpjSgnQzfAZDZD"


def connection():
    """
    Returns the GraphApi and checks if there was any error while connecting to Facebook
    :return:
    """
    api = ''
    try:
        api = facebook.GraphAPI(access_token=USER_TOKEN, version="2.12")
    except ConnectionError as error:
        writeStatusLog(503, error)
        print(f'Problemas de conexion: {error}')
    except Exception as error:
        writeStatusLog(404, error)
        print(error)
    writeStatusLog(200, 'You have successfully connected with the api')
    return api, True


def search_file():
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


def upload_to_albums(graph, caption, path):
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


def upload_photo(graph, caption):
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


def upload_post(graph):
    user_message = input("Que desea escribir?: ").capitalize()
    try:
        graph.put_object(parent_object='me', connection_name='feed', message=user_message)
    except Exception as error:
        print(f"Hubo un problema subiendo su post, error: {error}")


def get_post(graph):
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


def edit_post(graph):
    """
    The user can edit or delete a post made by them
    :param graph:
    :return:
    """
    post = get_post(graph)

    option = input("Desea eliminar el post o editar?: ").capitalize()

    if option == "Eliminar" or option == "Eliminarlo":
        graph.delete_object(id=post)
    elif option == "Editar" or option == "Editarlo":
        text = input("Que desea escribir: ").capitalize()
        graph.put_object(parent_object=post, connection_name='', message=text)
