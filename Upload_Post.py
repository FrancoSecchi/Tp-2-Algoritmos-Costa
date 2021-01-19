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


def main():
    data, isConnected = connection()
    if isConnected:
        user_message = input("Que desea escribir?: ").capitalize()
        data.put_object(parent_object='me', connection_name='feed',message= user_message)
        
main()