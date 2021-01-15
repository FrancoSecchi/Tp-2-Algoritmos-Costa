from pyfacebook import Api
import json  # Use the json module to write the files
import os
APP_ID = "432341101134225"
KEY_SECRET = "5f1a24aa9fc8ebd8f6e5cd26a1603ac3"  # The key changes through the time, check the app in facebook.developers
PAGE_ID = "103914631637231"
ACCESS_TOKEN = "EAAGJNkHBQZAEBAL8bEZARl3Q3GZCMNukGegto3gU9f8XNuxbreju755xKZATHwI389SMdh09qYZAZBZAZCxZAWhQFHoDEhqLME3OXRRJZAENytaOSl3HH08H8Qee92PF2bdvdAxmGNNFswyKdi5yu9wLawO7INU5ytSSAZA35XH2PLUtS2sZAvRZAzgJcwbZBH4GTuvGi1RcCZAyp89QgZDZD" # The key changes through the time, check the app in facebook.developers

# TODO Declare the necessary functions to carry out the draft


def connection():
    try:
        api = Api(app_id=APP_ID, app_secret=KEY_SECRET, long_term_token=ACCESS_TOKEN)
        return api, True
    except ConnectionError as error:
        print(f'Problemas de conexion: {error}')
    except Exception as error:
        print(error)

def search_file():
    #Searchs for a photo in the user desktop. The file must be .Jpg
    name = input("Ingrese el nombre del archivo: ")
    for root, dirs, files in os.walk(os.path.join(os.environ["HOMEPATH"], "Desktop")): 
        for file in files:  
            if file.endswith(name+".jpg"): 
                path ="C:"+ root + f"\{str(file)}"
    
    return path         

def upload_to_albums(graph,caption,path):
    #It needs the graph, a caption for the photo, and the path for said photo
    #It uploads it to an album which the user specifies
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
    
    graph.put_photo(image = open(path, 'rb'),album_path= albums_id[select-1]+ "/photos", message= caption)  

def upload_photo(graph,caption,path):
    #Needs the path of the picture. It uploads it with a caption written by the user
    path = search_file()
    try:
        graph.put_photo(image = open(path, 'rb'),message= caption)
    except FileNotFoundError:
        print("El archivo solicitado no se encuentra")    
    except Exception:
        print("Hubo un problema abriendo el archivo")  

def upload_post(graph):
    user_message = input("Que desea escribir?: ").capitalize()
    try:
        graph.put_object(parent_object='me', connection_name='feed',message= user_message)
    except Exception:
        print("Hubo un problema subiendo su post") 

def get_post(graph):
    #Fetch the ids of the last 5 posts and display them in some sort of menu 
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
    
    return posts_id[option-1]

def edit_post(graph):
    #The user can edit or delete a post made by them
    post = get_post(graph)
    
    option = input("Desea eliminar el post o editar?: ").capitalize()
    
    if option == "Eliminar" or option == "Eliminarlo":
        graph.delete_object(id=post)
    elif option == "Editar" or option == "Editarlo":    
        text = input("Que desea escribir: ").capitalize()       
        graph.put_object(parent_object= post, connection_name='', message= text)

def main():
    data, isConnected = connection()
    if isConnected:
        print(data.get_token_info())


main()
