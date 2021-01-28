import facebook
import json

USER_TOKEN = "EAAGJNkHBQZAEBAJcChJLpKyFkbkznqkbH28iHU2ubzr2Nbmmai3QiBgZAv36OM6mUZBaqYrrxEi6T3ppStt27kpQX8tKT5xwZBO3ZBZAQ3HzAxtVPrEtwHa9ZC7f8TtxaotCsrdx08OYqXFPkLbInISjx0NPg9HGwL0rOohzqm4VvKrnRY9UXno"

def connection():
    api = ''
    try:
        api = facebook.GraphAPI(access_token= USER_TOKEN, version="2.12")
    except ConnectionError as error:
        print(f'Problemas de conexion: {error}')
    except Exception as error:
        print(error)
    
    return api, True

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
        

def main():
    option = str
    graph, isConnected = connection()
    if isConnected:
        post = get_post(graph)
    
    option = input("Desea eliminar el post o editar?: ").capitalize()
    
    if option == "Eliminar" or option == "Eliminarlo":
        graph.delete_object(id=post)
    elif option == "Editar" or option == "Editarlo":    
        text = input("Que desea escribir: ").capitalize()       
        graph.put_object(parent_object= post, connection_name='', message= text)
        
        
main()