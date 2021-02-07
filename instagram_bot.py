from instabot import Bot
from logs import write_status_log


# ESTO SE USA PARA TESTEAR EL TRAINER.TXT
def hello():
    print("Uesa kpo desde instagram")


def connection_instagram(username='crux.bot', password='crux123') -> object:
    """
    PRE: The parameter can't be null
    :param username:
    :param password:
    :return:
    """
    instaBot = Bot()
    try:
        instaBot.login(username=username, password=password)
    except ConnectionError as error:
        write_status_log(503, error)
        raise ConnectionError(f'You dont have internet: {error}')
    except Exception as error:
        write_status_log(500, error)
        raise Exception(error)
    write_status_log(200, 'You have successfully connected with the Instagram bot')
    print('You have successfully connected with the Instagram bot')

    return instaBot


def search_users(bot) -> None:
    """
    PRE: The parameter can't be null
    :param bot:
    :return:
    """
    query = input("Who do you want to search? ")
    bot.search_users(query=query)
    bot.upload_photo()
    json_data = bot.last_json
    if json_data['num_results'] > 0:
        print("The users found are \n")
        for user in json_data['users']:
            full_data = ''
            full_data += f"{user['username']} {'Its a private profile' if user['is_private'] else 'Its a public profile'}"
            if 'social_context' in user.keys():
                full_data += f" Someone you know follows this account: {user['social_context']}"

    else:
        print("")


def follow_actions(bot, username, type_follow='follow') -> bool or Exception:
    """
    PRE: The parameter can't be null
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
