import facebook
import json
import os

INSTAGRAM_USER = 'crux.bot'
INSTAGRAM_PASS = 'crux123'
USER_TOKEN = "EAAGJNkHBQZAEBAPaFOXzg1ZBiEiKcmHJlKEOQCygEwsH20hhYlqc9mmPZCEv3pbfxIHR7qxEykjKniz38wZAZASrxZCDiFKu4ICZBvWjEJqB22N2BRc2ClIrlJ2gMXuYn63SdYsBsco1K17ITTgcuRL20esIzhehdh91MZBXsuFDL0AYff9kKrFBQ2uHuSoow9nfVpjSgnQzfAZDZD"


def connection():
    # Returns the GraphApi and checks if there was any error while connecting to Facebook
    api = ''
    try:
        api = facebook.GraphAPI(access_token=USER_TOKEN, version="2.12")
    except ConnectionError as error:
        print(f'Problemas de conexion: {error}')
    except Exception as error:
        print(error)
    return api, True


def get_albums(graph, caption, path):
    # It needs the graph, a caption for the photo, and the path for said photo
    # It uploads it to an album which the user specifies
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


def search_file() -> str:
    # Searchs for a photo in the user desktop. The file must be .Jpg
    name = input("Ingrese el nombre del archivo: ")
    path = ''
    for root, dirs, files in os.walk(os.path.join(os.environ["HOMEPATH"], "Desktop")):
        for file in files:
            if file.endswith(name + ".jpg"):
                path = "C:" + root + f"\{str(file)}"

    return path


def main():
    option = str
    graph, isConnected = connection()
    if isConnected:
        path = search_file()
        caption = input("Pie de Foto: ").capitalize()
        while option != "Si" or option != "No":
            option = input("Desea subirla a un album?: ").capitalize()

        if option == "Si":
            get_albums(graph, caption, path)
        elif option == "No":
            try:
                graph.put_photo(image=open(path, 'rb'), message=caption)
            except FileNotFoundError:
                print("El archivo solicitado no se encuentra")
            except Exception:
                print("Hubo un problema abriendo el archivo")


main()