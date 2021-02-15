from instabot import Bot
from logs import write_status_log, write_chat_bot, user_options, GET_NAME
import json
import codecs
import os.path
from termcolor import cprint

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys
    
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def edit_profile(bot) -> None or Exception:
    """
    PRE:
    POST:
    :param bot:
    :return:
    """
    my_profile = bot._call_api('accounts/current_user/', query = {'edit': 'true'})
    text_to_log = "Your actual profile is: \n"
    genders = ['male', 'female', 'unspecified']
    print(text_to_log)
    attributes = {
        'Full name': 'full_name',
        'Private account': 'is_private',
        'Biography': 'biography',
        'External url': 'external_url',
        'Email': 'email',
        'Phone number': 'phone_number',
        'Gender': 'gender',
    }
    
    data_change = {}
    all_data = ''
    profile = my_profile['user']
    
    for key, attribute in attributes.items():
        if attribute == 'gender':
            all_data += f'{key} : {genders[int(profile[attribute])]}\n'
        else:
            all_data += f'{key} : {profile[attribute]}\n'
    
    print(all_data)
    text_to_log += all_data
    prepare_data(profile, attributes, data_change, genders)
    
    write_chat_bot(text_to_log)
    
    try:
        status_account = bot.set_account_private() if data_change['is_private'] else bot.set_account_public()
        result = bot.edit_profile(
            first_name = data_change['full_name'],
            biography = data_change['biography'],
            external_url = data_change['external_url'],
            email = data_change['email'],
            gender = int(data_change['gender']),
            phone_number = data_change['phone_number']
        )
        if result and status_account['status'] == 'ok':
            text = "Profile has been modified successfully!"
            write_chat_bot(text)
            cprint(text, 'green', attrs = ['bold'])
        else:
            text = "There was a problem updating the profile, please try again"
            write_chat_bot(text)
            cprint(text, 'red', attrs = ['bold'])
    
    except Exception as error:
        write_status_log(error, 'Failed')
        raise Exception(error)


def prepare_data(profile, attributes, data_change, genders):
    """
    PRE:
    POST:
    :param profile:
    :param attributes:
    :param data_change:
    :param genders:
    :return:
    """
    for key, attribute in attributes.items():
        if attribute == 'full_name':
            cprint("IMPORTANT!", 'red', attrs = ['bold', 'blink'])
            cprint(
                "If you have changed the full name 2 times within a period of 14 days, you will not be able to modify your full name, just leave it empty, the program will not be able to change the full name. Be aware of your decision",
                'red',
                attrs = ['bold'])
        change_attribute = input(f"Do you want to change {key}? yes/no: ".lower()) in ['yes', 'y', 'ye']
        if change_attribute:
            if attribute == 'is_private':
                print("To change your account from private to public or vice versa, enter public/private")
            elif attribute == 'gender':
                print("To change your gender, enter male/female/unspecified")
            
            new_data = input(f"Enter the new value for {key}: ")
            secure = input(f"Are you sure to change {key} to '{new_data}'? yes/no: ".lower()) in ['yes', 'y', 'ye']
            
            if secure:
                if attribute == 'is_private':
                    new_data = True if new_data.lower() in ['private', 'priv', 'p'] else False
                elif attribute == 'gender':
                    if new_data in genders:
                        new_data = int(genders.index(new_data)) + 1
                    else:
                        while new_data not in genders:
                            new_data = input("The gender you have selected does not correspond to those available (male / female / unspecified), please enter a valid one: ")
                        else:
                            new_data = int(genders.index(new_data)) + 1
                
                data_change[attribute] = new_data
            else:
                print(f"No changes have been made to the {key}")
        else:
            data_change[attribute] = profile[attribute]


def follow_actions(bot, type_follow = 'follow') -> bool or Exception or None:
    """
    PRE: The parameter can't be null
    POST:
    :param type_follow:
    :param bot:
    :return:
    """
    if type_follow != 'follow':
        results = show_followings(bot)
        username = input(f"Who do you want to {type_follow}? ")
        for user in results['users']:
            if user['username'] == username:
                if bot.friendships_destroy(user['pk']):
                    text = f"{username} has been successfully unfollowed!"
                    cprint(text, 'green', attrs = ['bold'])
                    write_chat_bot(text)
    
    else:
        show_search_users(bot)
        username = input(f"Who do you want to {type_follow}? ")
        try:
            user = bot.username_info(username)['user']
            user_id = user['pk']
            if bot.friendships_create(user_id = user_id):
                text = f"{username} has a private account, we have sent him a request with success!" if user['is_private'] else f"{username} has been followed with success!"
                cprint(text, 'green', attrs = ['bold'])
            else:
                text = "There was a problem performing the action, please try again"
                cprint(text, 'red', attrs = ['bold'])
                write_chat_bot(text)
        
        except Exception as error:
            write_status_log(error, 'Internal server error')
            raise Exception(error)


def show_followings(bot):
    """
    PRE:
    POST:
    :param bot:
    :return:
    """
    rank = bot.generate_uuid()
    user_id = bot.authenticated_user_id
    results = bot.user_following(user_id, rank)
    print("You are following: \n")
    for user in results['users']:
        print(f"{user['username']} \n")
    
    return results


def show_search_users(bot) -> None:
    """
    PRE: The parameter can't be null
    POST:
    :param bot:
    :return:
    """
    user_name = user_options(GET_NAME)
    query = input("Who do you want to search? ")
    write_chat_bot("Who do you want to search? ")
    write_chat_bot(query, user_name)
    
    results = bot.search_users(query = query)
    text_to_log = "The users found are \n"
    if results['num_results'] > 0:
        print(text_to_log)
        for user in results['users']:
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


# ------------ CONNECTION AND CREDENTIALS ---------------#


def to_json(python_object):
    """
    
    :param python_object:
    :return:
    """
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    """
    
    :param json_object:
    :return:
    """
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    """
    :param api: the actual Client object
    :param new_settings_file: The json file where the credentials will be saved
    :return:
    """
    cache_settings = api.settings
    try:
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default = to_json)
    except Exception as error:
        write_status_log(error, 'failed')
        raise Exception(error)


def connection_instagram(username = 'crux.bot', password = 'crux123') -> object:
    """
    PRE: If the user does not give us the credentials of their instagram user, we will use the crux data
    POST: Credentials are created to avoid re-logging, and the connection with the api is created
    :param username:
    :param password:
    :return:
    """
    device_id = None
    try:
        settings_file = 'credentials.json'
        if not os.path.isfile(settings_file):
            # If the credentials do not exist, do a new login
            insta_bot = Client(
                username, password,
                on_login = lambda x: onlogin_callback(x, settings_file))
        else:
            # If the credentials do not exist, do a new login
            try:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook = from_json)
            except Exception as error:
                write_status_log(error, 'failed')
                raise Exception(error)
            
            print('Reusing settings: {0!s}'.format(settings_file))
            
            device_id = cached_settings.get('device_id')
            insta_bot = Client(
                username, password,
                settings = cached_settings)
    
    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        # Credentials expired
        # It does a relogin but using ua, keys and such
        insta_bot = Client(
            username, password,
            device_id = device_id,
            on_login = lambda x: onlogin_callback(x, settings_file))
    
    except ClientLoginError as e:
        write_status_log(e, 'ClientLoginError')
        raise ClientLoginError(e)
    except ClientError as e:
        write_status_log('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response), 'ClientError')
        raise ClientError('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
    except Exception as e:
        write_status_log('Unexpected Exception: {0!s}'.format(e), 'Exception')
        raise Exception('Unexpected Exception: {0!s}'.format(e))
    
    write_status_log('It has been possible to connect successfully with instagram')
    cprint("It has been possible to connect successfully with instagram", 'green', attrs = ['bold'])
    
    return insta_bot
