from instabot import Bot
from logs import write_status_log, write_chat_bot, user_options, GET_NAME
import json
import codecs
import os.path
from termcolor import cprint, colored

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


def check_if_following(bot, username) -> bool:
    """
    
    :param bot:
    :param username:
    :return:
    """
    following = get_followings(bot, False)
    user_info = bot.username_info(username)
    can_get_feed = False
    if user_info['user']['is_private']:
        for users in following['users']:
            if user_info['user']['pk'] in users:
                can_get_feed = True
    else:
        can_get_feed = True
    
    return can_get_feed


def prepare_text(post, post_to_show, attribute, comments, **extra_data) -> tuple:
    """

    :param post:
    :param post_to_show:
    :param attribute:
    :return:
    """
    title = colored(" {}: \n".format(extra_data['text']), 'white', attrs = ['bold'])
    post_to_show += title
    if attribute == "likers":
        count_likes = int(post['like_count'])
        if extra_data['username'] == extra_data['username_bot']:
            if count_likes <= 5:
                for users in post[attribute]:
                    name = users['full_name'] if len(users['full_name']) else users['username']
                    post_to_show += "\t- " + name + '\n'
            else:
                post_to_show += "\t- " + post[attribute][0]['full_name'] + " +{} users \n".format(int(count_likes) - 1)
        else:
            post_to_show += f"\t- total likes: {count_likes} \n"
    else:
        comment_number = 1
        for comment in comments[attribute]:
            text_comment = f"\tNº{comment_number} - " + f"'{comment['text']}'"
            name = comment['user']['full_name'] if len(comment['user']['full_name']) else comment['user']['username']
            post_to_show += text_comment + f" by {name} with {comment['comment_like_count']} likes \n"
            comment_number += 1
    
    return post_to_show, title


def show_user_feed(bot, feed) -> None:
    """
    
    :param feed:
    :return:
    """
    number_post = 1
    post_to_show = ''
    for post in feed['items']:
        comments = bot.media_comments(post['pk'])
        
        indicator_post = colored("\nPost Nº{} \n".format(number_post), 'white', attrs = ['bold', 'underline'])
        title = colored('\n Caption: \n\t', 'white', attrs = ['bold'])
        
        if type(post["caption"]) == dict:
            post_to_show += indicator_post + title + f'"{post["caption"]["text"]}"' + "\n"
        else:
            post_to_show += indicator_post + title + f'' + "\n"
        
        attributes = {'likers': "Likes", 'comments': "Comments"}
        
        for attr, text in attributes.items():
            post_to_show, title = prepare_text(post, post_to_show, attr, comments, username = username, username_bot = username, text = text)
        
        number_post += 1
        print(post_to_show)
        write_chat_bot(post_to_show)
        post_to_show = ''


def validate_comment(feed, position_comment, bot):
    """
    
    :param feed:
    :param comment_post:
    :return:
    """
    correct_post = False
    while not correct_post:
        if not feed[position_comment[0] - 1]:
            cprint("The post doesnt exist, please enter a correct post number", 'red', attrs = ['bold'])
            position_comment[0] = int(input("Number post: "))
        else:
            correct_post = True
    
    correct_comment = False
    post = feed[position_comment[0] - 1]
    comments = bot.media_comments(post['pk'])
    
    while not correct_comment:
        if not comments['comments'][position_comment[1] - 1]:
            cprint("The comment doesnt exist, please enter a correct comment number", 'red', attrs = ['bold'])
            position_comment[1] = int(input("Number comment: "))
        else:
            correct_comment = True
    
    return position_comment


def post_like_comment(bot, feed):
    """
    
    :param bot:
    :param feed:
    :return:
    """
    if feed[0]:
        position_comment = input("Which comment would you like to post a like? enter the post number and comment number. Ej: 1, 2 : ").split(',')
        position_comment = [int(x.strip()) for x in position_comment]
        position_comment = validate_comment(feed, position_comment, bot)
        post_id = feed[position_comment[0] - 1]['pk']
        comments = bot.media_comments(post_id)['comments']
        id_comment = comments[position_comment[1] - 1]['pk']
        result = bot.comment_like(id_comment)
        if result['status'] == 'ok':
            cprint(f"The comment '{comments[position_comment[1] - 1]['text']}' has been liked correctly", 'green', attrs = ['bold'])
        else:
            cprint(f"The comment '{comments[position_comment[1] - 1]['text']}' could not be liked, please try again later", 'red', attrs = ['bold', 'underline'])


def likes_actions(bot, target = "comment") -> Exception or ClientError or None:
    """
    
    :param bot:
    :param target:
    :return:
    """
    try:
        show_search_users(bot, "Which user do you want to like the posts? ")
        write_chat_bot("Which user do you want to like the posts? \n Enter username: ")
        if target != "comment":
            username = input("Enter username: ")
            can_get_feed = check_if_following(bot, username)
            if can_get_feed:
                feed = bot.username_feed(username)
                if feed['items'][0]:
                    show_user_feed(feed)
                    number_post = int(input("Which post would you like to post a like? enter the Nº: "))
                    if number_post in [0, len(feed['items']) - 1]:
                        id_post = feed['items'][number_post]['pk']
                        result = bot.post_like(media_id = id_post)
                        if result['status'] == 'ok':
                            cprint("It has been liked correctly!", 'green', ['bold'])
                else:
                    cprint("The user has no posts", 'red', attrs = ['bold', 'underline'])
            else:
                cprint(f"You cannot access the feed of the user {username} because it is a private account that you do not follow, or because it has blocked you", 'red', attrs = ['bold', 'underline'])
        else:
            cprint("Your feeed: ", 'blue', attrs = ['bold'])
            feed = bot.username_feed(bot.username)['items']
            show_user_feed(bot, feed)
            post_like_comment(bot, feed)
            
    except Exception as error:
        raise Exception(error)


def edit_profile(bot) -> Exception or ClientError or None:
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


def prepare_data(profile, attributes, data_change, genders) -> None:
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
                "If you have changed the full name 2 times within a period of 14 days, you will not be able to modify your full name, just leave it empty, the program will not be able to change the full name.\n Be aware of your decision",
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


def follow_actions(bot, follow_type = 'follow') -> Exception or ClientError or None:
    """
    PRE: The parameter can't be null
    POST:
    :param follow_type:
    :param bot:
    :return:
    """
    if follow_type != 'follow':
        results = get_followings(bot)
        username = input(f"Who do you want to {follow_type}? ")
        for user in results['users']:
            if user['username'] == username:
                if bot.friendships_destroy(user['pk']):
                    text = f"{username} has been successfully unfollowed!"
                    cprint(text, 'green', attrs = ['bold'])
                    write_chat_bot(text)
    
    else:
        show_search_users(bot)
        username = input(f"Who do you want to {follow_type}? ")
        try:
            user = bot.username_info(username)['user']
            user_id = user['pk']
            if bot.friendships_create(user_id = user_id):
                text = f"{username} has a private account, we have sent him a request with success!" if user['is_private'] else f"{username} has been followed with success!"
                write_chat_bot(text)
                cprint(text, 'green', attrs = ['bold'])
            else:
                text = "There was a problem performing the action, please try again"
                cprint(text, 'red', attrs = ['bold'])
                write_chat_bot(text)
        
        except Exception as error:
            write_status_log(error, 'Internal server error')
            raise Exception(error)


def get_followings(bot, show = True, type_show = 'following') -> dict or list:
    """
    PRE:
    POST:
    :param show:
    :param type_show:
    :param bot:
    :return:
    """
    rank = bot.generate_uuid()
    user_id = bot.authenticated_user_id
    if type_show == 'following':
        results = bot.user_following(user_id, rank)
        text = "You are following: \n"
    else:
        results = bot.user_followers(user_id, rank)
        text = "Your followers: \n"
    
    if show:
        cprint(text, 'blue', attrs = ['bold', 'underline'])
        for user in results['users']:
            print(f"{user['username']} \n")
    
    return results


def show_search_users(bot, text = 'Who do you want to search?') -> None:
    """
    PRE: The parameter can't be null
    POST:
    :param text:
    :param bot:
    :return:
    """
    user_name = user_options(GET_NAME)
    query = input(text)
    write_chat_bot(text)
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


def to_json(python_object) -> dict:
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


def onlogin_callback(api, new_settings_file) -> None:
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
        settings_file = os.path.abspath('credentials/instagram_api.json')
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
            
            print('Reusing settings: {0!s} \n'.format(settings_file))
            
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
    
    write_status_log('You have successfully connected with the instagram!')
    write_chat_bot('You have successfully connected with the instagram!')
    cprint("You have successfully connected with the instagram! \n", 'green', attrs = ['bold'])
    
    return insta_bot
