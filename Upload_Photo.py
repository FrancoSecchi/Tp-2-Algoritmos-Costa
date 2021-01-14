import facebook
import json
import os

USER_TOKEN = "EAAGJNkHBQZAEBAHqXb1p0FNdntrwMbZBMltJyukiHrftzQqeJ6DeCGxGxqmkoT2629St7981FUQq0RtypFy6aitbh3qaKYrNCbax4CU2fZAG1OhVyaRtUPBu6hN01ezKihAkJKD8CPauc7l1TFEFdM5QdAl6oeTdHdGodTy6lAIVAUgIiW5ubPd9Da2wZCYZD"

def connection():
    #Returns the GraphApi and checks if there was any error while connecting to Facebook
    api = ''
    try:
        api = facebook.GraphAPI(access_token= USER_TOKEN, version="2.12")
    except ConnectionError as error:
        print(f'Problemas de conexion: {error}')
    except Exception as error:
        print(error)
    return api, True

def get_albums(graph,caption,path):
    #It needs the graph, a caption for the photo, and the path for said photo
    #It uploads it to an album which the user specifies
    counter = 1
    albums_id = []
    albums = graph.get_connections(id='me', connection_name='albums')
    info_list = albums['data']
    print("Sus albums son: ")
    for info in info_list[0:5]:
        print(f"{counter} -", info["name"])
        counter += 1
        albums_id.append(info["id"])

    select = int(input("Seleccione el album: "))
    graph.put_photo(image = open(path, 'rb'),album_path= albums_id[select-1]+ "/photos", message= caption)  

def search_file():
    #Searchs for a photo in the user desktop. The file must be .Jpg
    name = input("Ingrese el nombre del archivo: ")
    for root, dirs, files in os.walk(os.path.join(os.environ["HOMEPATH"], "Desktop")): 
        for file in files:  
            if file.endswith(name+".jpg"): 
                path ="C:"+ root + f"\{str(file)}"
    
    return path         

def main():
    graph, isConnected = connection()
    if isConnected:
        path = search_file()
        caption = input("Pie de Foto: ").capitalize()
        option = input("Desea subirla a un album?: ").capitalize()
        if option == "Si":
            get_albums(graph,caption,path)
        else:
            try:
                graph.put_photo(image = open(path, 'rb'),message= caption)
            except FileNotFoundError:
                print("El archivo solicitado no se encuentra")    
            except Exception:
                print("Hubo un problema abriendo el archivo")    
        
main()