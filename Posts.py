import facebook
import json

USER_TOKEN="EAAGJNkHBQZAEBABdue94HmAkr0rlIlKUmo5K3XHsYf07lG3pJAco5lU4rjFAmu9ZBej8tZAv49RaPjZBDhVzpltZCQoi4iHIeh5h2AEn0fOCvVtrxZAdfttDSSY5DQWIRzTuU7oDSAfIbHQw3IjmZCVofmiRQh6eqvGFeewd7ZBZCBKwSC1t72Upq04SKdVgjPbbt80qsese1VwZDZD"

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
    counter = 1
    posts_id = []
    posts = graph.get_connections(id='me', connection_name='posts')
    info_list = posts['data']
    print("Los posts son: ")
    for info in info_list:
        if 'message' in info:
            print(info["created_time"][0:10]+":"+info["message"])
            counter += 1
            posts_id.append(info["id"])
        elif 'story' in info:
            print(info["created_time"][0:10]+":"+info["story"])
            counter += 1
            posts_id.append(info["id"])
        elif 'story' or 'message' not in info:
            print(info["created_time"][0:10]) 
def main():
    graph, isConnected = connection()
    if isConnected:
        get_post(graph)

main()