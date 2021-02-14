from instabot import Bot
from instagram_private_api import Client
from logs import write_status_log, remove_file, write_chat_bot, user_options, GET_NAME


def connection_instagram(username='crux.bot', password='crux123') -> object:
    """
    PRE: The parameter can't be null
    POST:
    :param username:
    :param password:
    :return:
    """
    remove_file('config/crux.bot_uuid_and_cookie.json')
    instaBot = Bot()
    try:
        instaBot.login(username=username, password=password)
    except ConnectionError as error:
        write_status_log(error, 'Connection error')
        raise ConnectionError(f'You dont have internet: {error}')
    except Exception as error:
        write_status_log(error, 'Internal server error')
        raise Exception(error)
    write_status_log('You have successfully connected with the Instagram bot')
    write_chat_bot('You have successfully connected with the Instagram bot')
    print('You have successfully connected with the Instagram api!')

    return instaBot


def show_search_users(bot) -> None:
    """
    PRE: The parameter can't be null
    :param bot:
    :return:
    """
    user_name = user_options(GET_NAME)
    query = input("Who do you want to search? ")
    write_chat_bot("Who do you want to search? ")
    write_chat_bot(query, user_name)

    bot.search_users(query=query)
    json_data = bot.last_json
    text_to_log = "The users found are \n"
    if json_data['num_results'] > 0:
        print(text_to_log)
        for user in json_data['users']:
            full_data = ''
            full_data += f"{user['username']} {'Its a private profile' if user['is_private'] else 'Its a public profile'}"
            if 'social_context' in user.keys():
                full_data += f" Someone you know follows this account: {user['social_context']}"
            print(full_data)
            text_to_log += full_data + '\n'
        write_chat_bot(text_to_log)

    else:
        print("No user with that name was found \n")
        write_chat_bot("No user with that name was found \n")


def follow_actions(bot, type_follow='follow') -> bool or Exception:
    """
    PRE: The parameter can't be null
    :param type_follow:
    :param bot:
    :param username:
    :return:
    """
    show_search_users(bot)
    username = input(f"Who do you want to {type_follow}? ")
    try:
        user_id = bot.get_user_id_from_username(username)

        print(bot.last_json)
        if type_follow == 'follow':
            if bot.follow(user_id=user_id):
                print("Se ha seguido al usuario con exito!")
            else:
                print("Hubo un problemita capo")
        else:
            if bot.unfollow(user_id=user_id):
                print("Se ha seguido al usuario con exito!")
            else:
                print("Hubo un problemita capo")
    except Exception as error:
        write_status_log(error, 'Internal server error')
        raise Exception(error)