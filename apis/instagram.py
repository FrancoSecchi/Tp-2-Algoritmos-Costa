from instabot import Bot
from logs import (write_log, STATUS_FILE, get_credentials,
                  delete_file, print_write_chatbot, input_user_chat)
from utils import utils
from termcolor import cprint, colored
import codecs
import json
import logging
import os.path
import time

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError, __version__ as client_version)
except ImportError:
    import sys
    
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError, __version__ as client_version)


def is_following_user(api: Client, username: str, client_username: str = '') -> tuple:
    """
    Check if the current user follows the searched user. It is also used to know if I can access the user's feed
    
    Arguments:
        api (Client) : object instagram Client
        username (str) : The username of the requested person
        client_username (str) : The username registered for the bot functionality
        
    Returns:
          tuple (bool, bool) : Returns if the current user follows the searched user,
                               and also returns if the user who searched for the current user is himself
    """
    is_following = False
    own_feed = False
    if username != client_username:
        following = get_follows(api, False)
        user_info = api.username_info(username)
        if user_info['user']['is_private']:
            for users in following['users']:
                if user_info['user']['pk'] in users.values():
                    is_following = True
        else:
            is_following = True
    else:
        is_following = True
        own_feed = True
    
    return is_following, own_feed


def format_description_comment(presentation_post: str, comments_post: dict, attribute: str) -> str:
    """
    A string is structured so that the visualization of the comment data looks pretty
    
    Arguments:
        presentation_post (str) - String to be altered for data display
        comments_post (dict) - Post comments
        attribute (str) - Value of the key in which the comment data is located
    
    Returns:
        str - Altered string
    """
    comment_number = 1
    if attribute in comments_post.keys() and comments_post[attribute]:
        for comment in comments_post[attribute]:
            text_comment = f"\tNº{comment_number} - " + f"'{comment['text']}'"
            name = comment['user']['full_name'] if len(comment['user']['full_name']) else comment['user'][
                'username']
            presentation_post += text_comment + f" by {name} with {comment['comment_like_count']} likes \n"
            comment_number += 1
    return presentation_post


def prepare_text(post_data: dict, presentation_post: str, attribute: str, comments_post: dict,
                 **extra_data) -> tuple:
    """
    A string is structured so that the visualization of the post data looks pretty
    And the structure of the string would be of this style:
    Post Nºn
         Caption:
            "Message"
         Likes:
            - User 1
            - User 2
            ...
            - User n
         Comments:
            Nº1 - 'comment 1' by username user 1 with n likes
            Nº2 - 'comment 2' by username user 2 with n likes
            ...
            Nºn - 'comment n' by username user n with n likes
            
    Arguments:
        post_data (dict) : Dictionary that stores all the post data
        presentation_post (str): String to be altered for data display
        attribute (str) : Value of the key in which the likes or comments data is located
        comments_post (dict) : Post comments
    
    Returns:
        tuple (str, str) : The altered string and the title of the current section are returned
    """
    title = colored(" {}: \n".format(extra_data['text']), 'white', attrs = ['bold'])
    presentation_post += title
    if attribute == "likers":
        count_likes = int(post_data['like_count'])
        if extra_data['own_feed']:
            if count_likes <= 5:
                for users in post_data[attribute]:
                    name = users['full_name'] if len(users['full_name']) else users['username']
                    presentation_post += "\t- " + name + '\n'
            else:
                presentation_post += "\t- " + post_data[attribute][0]['full_name'] + " +{} users \n".format(
                    int(count_likes) - 1)
        else:
            presentation_post += f"\t- total likes: {count_likes} \n"
    else:
        presentation_post = format_description_comment(presentation_post, comments_post, attribute)
    
    return presentation_post, title


def show_user_feed(api: Client, feed: list, own_feed = False) -> None:
    """
    The feed of a user chosen by the current user is printed.
    
    Arguments:
        api (Client) - object instagram Client
        feed (list) - List containing all the user's posts
        own_feed (bool) - If it's the current user's feed
    
    Returns:
        None
    """
    number_post = 1
    presentation_post = ''
    for post_data in feed:
        comments_post = api.media_comments(post_data['pk'])
        
        indicator_post = colored("\nPost Nº{} \n".format(number_post), 'white', attrs = ['bold', 'underline'])
        title = colored('\n Caption: \n\t', 'white', attrs = ['bold'])
        
        if type(post_data["caption"]) == dict:
            presentation_post += indicator_post + title + f'"{post_data["caption"]["text"]}"' + "\n"
        else:
            presentation_post += indicator_post + title + f'' + "\n"
        
        attributes = {'likers': "Likes", 'comments': "Comments"}
        
        for attr, text in attributes.items():
            presentation_post, title = prepare_text(
                post_data,
                presentation_post,
                attr,
                comments_post,
                own_feed = own_feed,
                text = text)
        
        number_post += 1
        print_write_chatbot(presentation_post)
        presentation_post = ''


def validate_number_post(post_number: int, max_number: int) -> int:
    """
    Validates if the position of the post entered by the user is in a range of 0 and the number of posts - 1

    Arguments:
        post_number (int) : Post number
        max_number (int) : The number of posts - 1

    Returns:
        int - The position of the post
    """
    correct = False
    while not correct:
        if post_number < 0 or post_number >= max_number:
            print_write_chatbot(message = "Number post incorrect", color = 'red', attrs_color = ['bold'])
            post_number = int(input_user_chat("Enter a valid posting number: "))
            print_write_chatbot("Enter a valid posting number: ")
        else:
            correct = True
    return post_number


def validate_comment_number(comments, comment_number) -> int:
    """
    Validates if the position of the comment entered by the user is in dict with all comments
    
    Arguments:
        comments (dict) : Dict with all comments
        comment_number (int) : Position of the comment
    
    Returns:
        int - The position of the comment
    """
    correct_comment = False
    
    while not correct_comment:
        if not comments['comments'][comment_number]:
            print_write_chatbot(message = "The comment doesnt exist, please enter a correct comment number",
                                color = 'red', attrs_color = ['bold'])
            comment_number = int(input_user_chat("Number comment: "))
        
        else:
            correct_comment = True
    return comment_number


def validate_post_comment_number(api: Client, feed: dict, position_comment: list) -> list:
    """
    The position of the comment and the post is validated
    
    Arguments:
        api (Client) - object instagram Client
        feed (dict) - feed of the user
        position_comment (list) - position of post and comment
    
    Returns:
        list -  The position of the post and the comment
    """
    position_comment[0] = validate_number_post(post_number = position_comment[0], max_number = len(feed))
    post = feed[position_comment[0] - 1]
    comments = api.media_comments(post['pk'])
    position_comment[1] = validate_comment_number(comments = comments, comment_number = position_comment[1] - 1)
    
    return position_comment


def get_username(api: Client, text: str) -> str:
    """
    Search and return a valid username searched by the current user
    
    Arguments:
        api (Client) : object instagram Client
        text (str) : It's a personalized string which contains a
                     different questions depending by the current user want to do
    
    Returns:
        str - The username of the searched user
    """
    are_users = search_users(api, text)
    while not are_users:
        are_users = search_users(api, "No users with that name were found, please enter a correct name: ")
        print_write_chatbot("No users with that name were found, please enter a correct name: ")
    
    username = input_user_chat("Enter username: ")
    return username


def get_user_feed(api: Client, username: str = '', own_feed = False, show_feed = True) -> tuple:
    """
    Returns the feed of the searched user, and can print the feed
    
    Arguments:
        api (Client) : object instagram Client
        username (str) : the username of the searched user
        own_feed (bool) : If it's the current user's feed
        show_feed (bool) : If its must print the feed
    
    Returns:
        tuple (dict, bool) : the feed of the searched user and if the feed is empty
    """
    username_feed = api.username_feed(username) if not own_feed else api.self_feed()
    if show_feed:
        show_user_feed(api, feed = username_feed['items'], own_feed = own_feed)
    return username_feed, not username_feed['items'][0]


def post_comment(api: Client) -> None:
    """
    Post a comment on a post from a user chosen by the current user
    
    Arguments:
        api (Client) : object instagram Client
    
    Returns:
        None
    """
    username = get_username(api, "Who do you want to find to post a comment on his post?")
    
    can_get_feed, own_feed = is_following_user(api = api,
                                               username = username,
                                               client_username = api.username)
    
    if can_get_feed:
        feed, is_feed_empty = get_user_feed(api, username, own_feed = own_feed)
        if not is_feed_empty:
            comment_block = True
            text = "Which post would you like to comment on?"
            post_id, number_post = get_post_id(feed, text), get_post_number(text = text,
                                                                            max_cant_posts = len(
                                                                                feed['items']))
            want_put_comment = True
            while comment_block and want_put_comment:
                if 'comments_disabled' not in feed['items'][number_post]:
                    comment_block = False
                else:
                    print_write_chatbot(
                        message = "The post has the comments blocked, please choose another post\n",
                        color = 'red',
                        attrs_color = ['bold'])
                    another_try = input_user_chat("Do you want to try another comment? (yes/no) ")
                    
                    if utils.user_answer_is_yes(another_try):
                        post_id, number_post = get_post_id(feed, text), get_post_number(text = text,
                                                                                        max_cant_posts = len(
                                                                                            feed['items']))
                    else:
                        want_put_comment = False
            
            if want_put_comment:
                message = input_user_chat("Message: ")
                result = api.post_comment(media_id = post_id, comment_text = message)
                try:
                    if result['status'] == 'ok':
                        print_write_chatbot(message = "The comment has been posted correctly!\n", color = 'green',
                                            attrs_color = ['bold'])
                except Exception as error:
                    write_log(STATUS_FILE, str(error), 'Crux')
                    print_write_chatbot(f"There was an error: {error}", color = 'red', attrs_color = ['bold'])
            else:
                print_write_chatbot(
                    message = "It's okay if you couldn't leave a comment,"
                              " there are many posts in the sea, go get them tiger!\n",
                    color = 'blue', attrs_color = ['bold', 'underline'])
    else:
        print_write_chatbot(message = "You cant get the feed", color = 'red', attrs_color = ['bold'])


def get_post_number(text: str, max_cant_posts: int) -> int:
    """
    Returns the post number chosen by te current user
    
    Arguments:
        text (str) : It's a personalized string which contains a
                     different questions depending by the current user want to do
        max_cant_posts (str) : The maximum number of posts
    """
    post_number = int(input_user_chat(f"{text} enter the Nº: ")) - 1
    return validate_number_post(post_number, max_cant_posts)


def get_post_id(feed: dict, text: str) -> str:
    """
    Returns the id of the post
     
    Arguments:
        feed (dict) : the user feed
        text (str) : It's a personalized string which contains a
                     different questions depending by the current user want to do
    
    Returns:
        str - the id of the post
    """
    number_post = get_post_number(text = text, max_cant_posts = len(feed['items']))
    post_id = feed['items'][number_post]['pk']
    return post_id


def likes_actions(api: Client, target_type: str, like_type: str = 'like') -> None:
    """
    Depending on the type of target and type of like, a post or a comment will be liked or unlike
    
    Arguments:
        api (Client) : Object instagram Client
        target_type (str) : String that can be post or comment
        like_type (str) : String that can be like or unlike
    
    Returns:
        None
    """
    try:
        if target_type != "comment":
            username = get_username(api, f"\nWhich user do you want to {like_type} the {target_type}?")
            can_get_feed = is_following_user(api, username)
            if can_get_feed:
                feed, is_feed_empty = get_user_feed(api, username = username, show_feed = False)
                if not is_feed_empty:
                    own_feed = username == api.username
                    show_user_feed(api, feed['items'], own_feed = own_feed)
                    post_id = get_post_id(feed = feed, text = f"Which post would you {like_type} to post a like?")
                    if like_type == 'like':
                        like_post(api, post_id = post_id, own_feed = own_feed)
                    else:
                        unlike_post(api, post_id)
                else:
                    print_write_chatbot(message = "The user has no posts\n", color = 'red',
                                        attrs_color = ['bold', 'underline'])
            else:
                print_write_chatbot(
                    message = f"You cannot access the feed of the user {username} "
                              f"because it is a private account that you do not follow, "
                              f"or because it has blocked you\n",
                    color = 'red',
                    attrs_color = ['bold', 'underline'])
        else:
            print_write_chatbot(message = "Your feed: ", color = 'blue', attrs_color = ['bold'])
            feed, is_feed_empty = get_user_feed(api, own_feed = True)
            if not is_feed_empty:
                text = f"Which comment would you like to post a {like_type}?"
                comment_data = prepare_comment(api = api, feed = feed['items'], text = text)
                if like_type == 'like':
                    like_comment(api, comment_id = comment_data["comment_id"], own_feed = True)
                else:
                    unlike_comment(api, comment_id = comment_data["comment_id"])
            else:
                print_write_chatbot(message = "Your feed is empty", color = 'red', attrs_color = ['bold'])
    
    except Exception as error:
        write_log(STATUS_FILE, f"There was an error:{error}", 'Crux')
        print_write_chatbot(f"There was an error:{error}", color = 'red', attrs_color = ['bold'])


def already_liked(api: Client, target_id: str, type_like: str = 'post', own_feed: bool = False) -> bool:
    """
    Check if the post / comment is already liked by the current user
    
    Arguments:
        api (Client) : Object instagram Client
        target_id (str) : Id of comment or post
        type_like (str) : String that can be post or comment
        own_feed (bool) : If it's the current user's feed
        
    Returns:
        bool - if the post or comment is already liked
    
    """
    is_liked = False
    if type_like == 'post':
        likes = api.media_likers(target_id)['users']
    else:
        likes = api.comment_likers(target_id)
    
    bot_id = int(api.authenticated_user_id)
    
    if likes:
        collection_likes = likes['users'] if own_feed else likes
        
        for likers in collection_likes:
            if bot_id == likers['pk']:
                is_liked = True
    
    return is_liked


def unlike_comment(api: Client, comment_id: str) -> None:
    """
    Put a unlike in a comment chosen by the user
    
    Arguments:
        api (Client) : object instagram Client
        comment_id (str) : Id of the comment
    
    Returns:
        None
    """
    result = api.comment_unlike(comment_id)
    
    if result['status'] == 'ok':
        print_write_chatbot(f"The comment is unliked correctly!\n", color = 'green', attrs_color = ['bold'])
    
    else:
        print_write_chatbot(f"There was a problem disliking the comment, please try again later!\n",
                            color = 'red', attrs_color = ['bold'])


def unlike_post(api: Client, post_id: str) -> None:
    """
    Put a unlike in a post chosen by the user

    Arguments:
        api (Client) : Object instagram Client
        post_id (str) : Id of the post
    
    Returns:
    
    """
    result = api.delete_like(post_id)
    
    if result['status'] == 'ok':
        print_write_chatbot(f"The post is unliked correctly!\n", color = 'green', attrs_color = ['bold'])
    
    else:
        print_write_chatbot(f"There was a problem disliking the post, please try again later!\n",
                            color = 'red', attrs_color = ['bold'])


def like_comment(api: Client, comment_id: str, own_feed: bool = False):
    """
    Put a like in a comment chosen by the user

    Arguments:
        api (Client) : object instagram Client
        comment_id (str): Id of the comment
        own_feed (bool) : If it's the current user's feed
    
    Returns:
         None
    """
    if not already_liked(api, comment_id, type_like = 'comment', own_feed = own_feed):
        result = api.comment_like(comment_id = comment_id)
        if result['status'] == 'ok':
            text = "The comment has been liked correctly!\n"
            print_write_chatbot(text, color = 'green', attrs_color = ['bold'])
        else:
            print_write_chatbot(f"There was a problem liking the comment, try again later!\n", color = 'red',
                                attrs_color = ['bold', 'underline'])
    else:
        if want_unlike_target('comment'):
            unlike_comment(api, comment_id)
        else:
            print_write_chatbot("The like has been left as it was\n")


def want_unlike_target(target_type: str) -> bool:
    """
    The user is asked if he wants to leave a dislike in a comment or post
    
    Arguments:
        target_type (str) : String that can be post or comment
    
    Returns:
        bool - If the user wants to leave a dislike in the target
    """
    do_unlike = input_user_chat(f"The {target_type} is already"
                                f" liked by you, you want to unliked? (yes/no): ".lower())
    return utils.user_answer_is_yes(do_unlike)


def like_post(api: Client, post_id: str, own_feed: bool = False) -> None:
    """
    Put a like in a post chosen by the user

    Arguments:
        api (Client) : object instagram Client
        post_id (str) : Id of the post
        own_feed (bool) : If it's the current user's feed
        
    Return:
        None
    """
    if not already_liked(api, post_id, own_feed = own_feed):
        result = api.post_like(media_id = post_id)
        if result['status'] == 'ok':
            text = "The post has been liked correctly!\n"
            print_write_chatbot(text, color = 'green', attrs_color = ['bold'])
        else:
            print_write_chatbot(f"There was a problem liking the post, try again later!\n", color = 'red',
                                attrs_color = ['bold', 'underline'])
    else:
        
        if want_unlike_target('post'):
            unlike_post(api, post_id)
        else:
            print_write_chatbot("The like has been left as it was\n")


def prepare_comment(api: Client, feed: dict, text: str) -> dict:
    """
    The user is asked for the number of the post and the comment and the data is validated to be correct
    
    Arguments:
        api (Client) : object instagram Client
        feed (dict) : Feed of the user
        text (str) : It's a personalized string which contains a
                     different questions depending by the current user want to do
    
    Returns:
        dict - dict which contains the id of the post and the id of the comment
    """
    position_comment = input_user_chat(f"{text} enter the post number and comment number. Ej: 1, 2 : ").split(',')
    position_comment = [int(x.strip()) for x in position_comment]
    
    position_comment = validate_post_comment_number(api, feed, position_comment)
    post_id = str(feed[position_comment[0] - 1]['pk'])
    comments = api.media_comments(post_id)['comments']
    comment_id = str(comments[position_comment[1] - 1]['pk'])
    
    return {'post_id': post_id, 'comment_id': comment_id}


def show_profile_data(profile: dict, attributes: dict, genders: list) -> str:
    """
    The personal data values that are available for editing are printed on the screen.
    
    Arguments:
        profile (dict) : The profile data
        attributes (dict) : Dict which contains all available attributes for edit
        genders (list) : List of the available genders
    
    Returns:
        str - Formatted string with the profile data
    """
    presentation_profile_data = ''
    for key, attribute in attributes.items():
        if attribute == 'gender':
            presentation_profile_data += f'{key} : {genders[int(profile[attribute]) - 1]}\n'
        else:
            presentation_profile_data += f'{key} : {profile[attribute]}\n'
    
    print_write_chatbot(presentation_profile_data)
    return presentation_profile_data


def edit_profile(api: Client) -> None:
    """
    Available personal data is edited.
    What are full name, private account, biography, url, email, phone number and gender
    
    Arguments:
        api (Client) - object Client instagram
    Returns:
        None
    """
    
    # I call _call_api because the original function "current_user" was passing wrong parameters
    # and the request was not made correctly
    user_profile = api._call_api('accounts/current_user/', query = {'edit': 'true'})['user']
    text_to_print = "Your actual profile is: \n"
    genders = ['male', 'female', 'unspecified']
    print_write_chatbot(text_to_print)
    attributes = {
        'Full name': 'full_name',
        'Private account': 'is_private',
        'Biography': 'biography',
        'External url': 'external_url',
        'Email': 'email',
        'Phone number': 'phone_number',
        'Gender': 'gender',
    }
    
    new_profile_data = {}
    
    all_data = show_profile_data(user_profile, attributes, genders)
    
    text_to_print += all_data
    get_new_profile_data(user_profile, attributes, new_profile_data, genders)
    
    print_write_chatbot(text_to_print)
    
    try:
        status_account = api.set_account_private() if new_profile_data['is_private'] else api.set_account_public()
        result = api.edit_profile(
            first_name = new_profile_data['full_name'],
            biography = new_profile_data['biography'],
            external_url = new_profile_data['external_url'],
            email = new_profile_data['email'],
            gender = int(new_profile_data['gender']),
            phone_number = new_profile_data['phone_number']
        )
        if result and status_account['status'] == 'ok':
            text = "Profile has been modified successfully!"
            print_write_chatbot(message = text, color = 'green', attrs_color = ['bold'])
        else:
            text = "There was a problem updating the profile, please try again\n"
            print_write_chatbot(message = text, color = 'red', attrs_color = ['bold'])
    
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Crux')
        print_write_chatbot(f"There was an error:{error}", color = 'red', attrs_color = ['bold'])


def get_new_profile_data(profile_data: dict, attributes: dict, new_profile_data: dict, genders: list) -> None:
    """
    The user is asked for the new values for the personal data of the profile,
    and the values are stored in the new_profile_data dictionary
    
    Arguments:
        profile_data (dict) : All personal account data
        attributes (dict) : Stores all available fields that can be changed
        new_profile_data (dict) : Empty dictionary that will store the new values
        genders (list) : List of available genres
    
    Returns:
        None
    """
    for key, attribute in attributes.items():
        if attribute == 'full_name':
            print_write_chatbot("IMPORTANT!\n", color = 'red', attrs_color = ['bold', 'blink'])
            print_write_chatbot(
                "If you have changed the full name 2 times within a period of 14 days, "
                "you will not be able to modify your full name, just leave it empty,"
                " the program will not be able to change the full name.\n Be aware of your decision\n",
                color = 'red',
                attrs_color = ['bold'])
        
        change_attribute = input_user_chat(f"Do you want to change {key}? yes/no: ")
        
        if utils.user_answer_is_yes(change_attribute):
            if attribute == 'is_private':
                print_write_chatbot(
                    "\nTo change your account from private to public or vice versa, enter public/private")
            
            elif attribute == 'gender':
                print_write_chatbot("\nTo change your gender, enter male/female/unspecified")
            
            new_data = input_user_chat(f"Enter the new value for {key}: ")
            
            secure = input_user_chat(f"\nAre you sure to change {key} to '{new_data}'? yes/no: ")
            
            if utils.user_answer_is_yes(secure):
                if attribute == 'is_private':
                    new_data = True if new_data.lower() in ['private', 'priv', 'p'] else False
                elif attribute == 'gender':
                    if new_data in genders:
                        new_data = int(genders.index(new_data)) + 1
                    else:
                        while new_data not in genders:
                            new_data = input_user_chat(
                                "The gender you have selected does not correspond"
                                " to those available (male / female / unspecified), please enter a valid one: ")
                        else:
                            new_data = int(genders.index(new_data)) + 1
                
                new_profile_data[attribute] = new_data
            else:
                print_write_chatbot(f"No changes have been made to the {key}")
        else:
            new_profile_data[attribute] = profile_data[attribute]


def delete(api: Client, target_id: str, target_type: str, parent_id: str = '') -> None:
    """
    Delete a post or comment chosen by the current user
    
    Arguments:
        api (Client) : Object instagram Client
        target_id (str) : Id of the post or comment to delete
        target_type (str) : String that can be post or comment
        parent_id (str) : In the event that a comment is deleted,
                          it stores the id of the post that contains said comment,
                          
    Returns:
        None
    """
    
    if target_type == 'post':
        result = api.delete_media(media_id = target_id)
    else:
        result = api.delete_comment(media_id = parent_id, comment_id = target_id)
    
    if result['status'] == 'ok':
        print_write_chatbot(f"The {target_type} has been successfully removed!\n", color = 'green',
                            attrs_color = ['bold'])
    
    else:
        print_write_chatbot(f"The {target_type} could not be removed. Please try again later\n", color = 'red',
                            attrs_color = ['bold'])


def delete_comment(api: Client, feed: dict) -> None:
    """
    Delete a comment chosen by the current user
    
    Arguments:
        api (Client) : Object instagram Client
        feed (dict) : the user feed
    
    Returns:
        None
    """
    print_write_chatbot("You cannot edit a comment, only delete it\n", color = 'blue',
                        attrs_color = ['bold', 'underline'])
    secure_delete = input_user_chat("Do you want to delete a comment from a post? (yes/no): \n")
    
    if utils.user_answer_is_yes(secure_delete):
        text = "Which comment would you delete?"
        comment_data = prepare_comment(api = api, feed = feed['items'], text = text)
        delete(api, target_id = comment_data['comment_id'], target_type = 'comment',
               parent_id = comment_data['post_id'])


def edit_post(api: Client, feed: dict, post_id: str, number_post: int) -> None:
    """
    Edit a post chosen by the current user
    
    Arguments:
        api (Client) : Object instagram Client
        feed (dict) : the user feed
        post_id (str) : Id of the post
        number_post (int) : Position of the post in the items feed
    
    """
    print_write_chatbot("You can only edit the caption!\n", color = 'blue', attrs_color = ['bold', 'blink'])
    old_caption = feed['items'][number_post]['caption']['text']
    new_caption = input_user_chat("Enter the new caption: ")
    secure = input_user_chat(f"\nAre you sure to change '{old_caption}' to '{new_caption}'? (yes/no): ")
    
    if utils.user_answer_is_yes(secure):
        result = api.edit_media(media_id = post_id, caption = new_caption)
        if result['status'] == 'ok':
            print_write_chatbot("It has been edited successfully!\n", color = 'green', attrs_color = ['bold'])
        
        else:
            print_write_chatbot(message = "An error occurred while changing it, please try again later\n",
                                color = 'red', attrs_color = ['bold'])
    
    else:
        print_write_chatbot("The post has not been modified\n", color = 'blue', attrs_color = ['bold'])


def edit_actions(api: Client, edit_type: str, target_type: str = 'post') -> None:
    """
    Depending on the type of target and type of like, a post or a comment will be edit or delete
    
    Arguments:
        api (Client) : Object instagram Client
        edit_type (str) : Can be delete or edit
        target_type (str) : Can be post or comment

    Returns:
        None
    """
    feed = api.self_feed()
    is_feed_empty = feed['items'][0]
    
    if is_feed_empty:
        if target_type == 'post':
            text = f"Which post would you {edit_type}?"
            post_id, number_post = get_post_id(feed, text = text), get_post_number(text, len(feed['items']))
            if edit_type == 'edit':
                edit_post(api, feed, post_id, number_post)
            else:
                secure = input_user_chat(f"Are you sure to {edit_type} the post? (yes/no): \n")
                if utils.user_answer_is_yes(secure):
                    delete(api, post_id, 'post')
        else:
            if edit_type == 'delete':
                delete_comment(api, feed)
    else:
        print_write_chatbot("Your feed is empty", color = 'red', attrs_color = ['bold'])


def unfollow(api: Client) -> None:
    """
    Users who are followed by the current user are obtained
    and one of them chosen by the current user is unfollowed
    
    Arguments:
        api (Client) : Object instagram Client
    
    Returns:
        None
    """
    try:
        results = get_follows(api)
        username = input_user_chat(f"Who do you want to unfollow? ")
        for user in results['users']:
            if user['username'] == username:
                if api.friendships_destroy(user['pk']):
                    text = f"{username} has been successfully unfollowed!"
                    print_write_chatbot(message = text, color = 'green', attrs_color = ['bold'])
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Crux')
        print(f"There was an error:{error}")


def follow(api: Client) -> None:
    """
    A specific user was searched and that user will be followed by the current user
    
    Arguments:
        api (Client) : Object instagram Client
    
    Returns:
        None
    """
    try:
        search_users(api)
        username = input_user_chat(f"Who do you want to follow? ")
        user = api.username_info(username)['user']
        user_id = user['pk']
        if api.friendships_create(user_id = user_id):
            text = f"{username} has a private account, we have sent him a request with success!" if user[
                'is_private'] else f"{username} has been followed with success!"
            print_write_chatbot(message = text, color = 'green', attrs_color = ['bold'])
        else:
            text = "There was a problem performing the action, please try again"
            print_write_chatbot(message = text, color = 'red', attrs_color = ['bold'])
    
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Crux')
        print_write_chatbot(f"There was an error:{error}", color = "red", attrs_color = ['bold'])


def get_follows(api: Client, show: bool = True, follow_type: str = 'following') -> dict:
    """
    Depending on the follow_type, a dictionary will be obtained
    that contains the users who follow the current user or those that the current user is following
    
    Arguments:
        api (Client) : Object instagram Client
        show (bool) : Indicates whether the filtered user names should be printed or not
        follow_type (str) : Can be following or followed
    
    Returns:
        None
    """
    rank = api.generate_uuid()
    user_id = api.authenticated_user_id
    if follow_type == 'following':
        results = api.user_following(user_id, rank)
        prefix = "You are"
    else:
        results = api.user_followers(user_id, rank)
        prefix = "Your"
    
    text = f"{prefix} {follow_type}: \n"
    
    if show:
        print_write_chatbot(text, color = 'blue', attrs_color = ['bold', 'underline'])
        for user in results['users']:
            print_write_chatbot(f"{user['username']}")
    
    return results


def search_users(api, text: str = 'Who do you want to search?') -> bool:
    """
    The user is prompted for a username to find an account with that username,
    and 50 similar users with that username are printed
    
    Arguments:
        api (Client) : Object instagram Client
        text (str) : It's a personalized string which contains a
                     different questions depending by the current user want to do
    
    Returns:
        bool - If users with that username were found
    """
    query = input_user_chat(text)
    
    results = api.search_users(query = query)
    if results['num_results'] > 0:
        print_write_chatbot("The maximum number of users to display is 50\n The users found are \n")
        for user in results['users']:
            full_data = ''
            full_data += f"{user['username']} {'Its a private profile' if user['is_private'] else 'Its a public profile'}"
            if 'social_context' in user.keys():
                full_data += f" Someone you know follows this account: {user['social_context']}"
            if user['friendship_status']['following']:
                full_data += colored(f" You are currently following it", 'green')
            
            print_write_chatbot(full_data + "\n")
        are_users = True
    else:
        are_users = False
        print_write_chatbot("No user with that name was found", color = "red", attrs_color = ['bold'])
    
    return are_users


def prepare_format_message(conversations: dict, its_me: str) -> str:
    """
    A string is structured so that the visualization of the post data looks pretty.
    Depending on the last type of chat event, data corresponding to said event will be added to the string

    Arguments:
        conversations (dict) : A dict which contains the last events of all chats
        its_me (bool) : If the last chat event was sent by the current user
    
    Returns:
        str - Formatted string with the data of the last events of the chats
    """
    message = ''
    if conversations['items'][0]['item_type'] == 'media':
        message += f"\t\t-({its_me}) Its a image, url: " + \
                   f"{conversations['items'][0]['media']['image_versions2']['candidates'][0]['url']} \n"
    
    elif conversations['items'][0]['item_type'] == 'text':
        message += f"\t\t-({its_me}) Text: {conversations['items'][0]['text']}\n"
    
    elif conversations['items'][0]['item_type'] == 'media_share':
        image = conversations['items'][0]['media_share']['image_versions2']['candidates'][0]['url']
        user_post = conversations['items'][0]['media_share']['users']['username']
        caption = conversations['items'][0]['media_share']['caption']['text']
        url_post = f"https://instagram.com/p/{conversations['items'][0]['media_share']['code']}/"
        message += f"\t\t-({its_me}) It is a publication \n From :{user_post} \n " \
                   f"Url: {url_post} \n Image: {image} \n Caption: '{caption}' \n"
    
    elif conversations['items'][0]['item_type'] == 'profile':
        username = conversations['items'][0]['media_share']['users'][0]['username']
        url_post = f"https://instagram.com/{username}/"
        message += f"\t\t-({its_me}) It is a profile \n Url: {url_post} \n"
    
    elif conversations['items'][0]['item_type'] == 'placeholder':
        message += f"\t\t-({its_me}) It is a reel, please open it on the cell phone\n"
    
    elif conversations['items'][0]['item_type'] == 'action_log':
        message += f"\t\t-({its_me}) It is a action, " \
                   f"{conversations['items'][0]['action_log']['description']} \n"
    
    return message


def show_last_messages(last_messages: dict, bot_id: str) -> None:
    """
    Print the last events of the chats of the current user
    
    Arguments:
        last_messages (dict) : Dict which contains all the information of the last event for each chat
        bot_id (str): Id of the current instagram account
        
    Returns:
        None
    """
    text_show = ''
    message_number = 1
    title = colored('Messages: \n', 'white', attrs = ['bold'])
    text_show += title
    text_to_bot = 'Messages: \n'
    chat_messages = last_messages['threads']
    if chat_messages:
        for conversations in last_messages['threads']:
            user = conversations['users'][0]['full_name']
            text_show += colored(f"\t-Nº{message_number} - {user}: \n", 'white', attrs = ['bold'])
            text_to_bot += f"\t-Nº{message_number} - {user}: \n"
            i_sent = conversations['items'][0]['user_id'] == int(bot_id)
            its_me = "You sent" if i_sent else "He sent"
            message = prepare_format_message(conversations, its_me)
            text_show += message
            message_number += 1
        print_write_chatbot(text_show)
    else:
        print_write_chatbot("You don't have any chat\n", color = 'red', attrs_color = ['bold'])


def validate_message() -> str:
    """
    Validate that the message you want to send to a user is not empty
    
    Arguments:
        -
    
    Returns:
        str - Validated message
    """
    validated = False
    message = ''
    while not validated:
        message = input_user_chat("Message: ")
        if message:
            validated = True
    
    return message


def send_message(api: Client) -> None:
    """
    The user is asked for a message and is sent to the username selected
    
    Arguments:
        api(client): client object of Instagram
        
     Returns:
        None
    """
    print_write_chatbot("Please wait a few seconds\n", color = 'blue', attrs_color = ['bold'])
    text = "Who do you want to send a message to?"
    aux_api = connection_aux_api(api.username, api.password)
    username = get_username(api, text)
    message = validate_message()
    user_info = api.username_info(username)
    result = aux_api.send_message(message, str(user_info['user']['pk']))
    if result:
        print_write_chatbot(f"The message has been sent to {username} correctly!\n", color = 'green',
                            attrs_color = ['bold'])
    else:
        print_write_chatbot(f"The message was not sent to {username} correctly, please try again later\n",
                            color = 'red', attrs_color = ['bold'])


def message_actions(api: Client, action_type: str = 'send') -> None:
    """
    The last events of each chat of the current user
    will be shown or a message will be sent to a user chosen by the current user
    
    Arguments:
        api(client): client object of Instagram
        action_type (str) : Can be send or show
    
     Returns:
        None
    """
    print_write_chatbot("IMPORTANT!!\n", color = 'red', attrs_color = ['bold', 'blink', 'underline'])
    print_write_chatbot(
        "Thanks to Mark Zuckerberg, we can only show the latest events from each chat"
        ".\nWhether it is a like to a comment, share a profile / reel / publication / a message\n",
        color = 'red',
        attrs_color = ['bold', 'underline'])
    
    try:
        if action_type != 'send':
            last_messages = api.direct_v2_inbox()['inbox']
            show_last_messages(last_messages, api.authenticated_user_id)
        else:
            send_message(api)
    
    except Exception as error:
        print(f"There was an error:{error}")


# ------------ CONNECTIONS AND CREDENTIALS ---------------#

def to_json(python_object) -> dict:
    """

    """
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    """
    """
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def on_login_callback(api: Client, new_settings_file: str) -> None:
    """
    Write, in a json, the cookies and settings to avoid re-login
    
    Arguments:
        api (Client): the actual Client object
        new_settings_file (str): The json file where the credentials will be saved
    Returns:
        None
    """
    cache_settings = api.settings
    try:
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default = to_json)
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Crux')
        print(f"There was an error:{error}")


def delete_cookie(file: str) -> None:
    """
    If more than 1 hour has passed, the cookie will be deleted to avoid errors
    
    Arguments:
        file (str) : The relative path of the cookie file
    
    Returns:
        None
    """
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        create_time = data['created_ts']
        now = time.time()
        if (create_time + 3600) <= round(now):
            delete_file(file)
            cprint("Cookie removed", 'yellow', attrs = ['bold'])
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Crux')
        print(f"There was an error:{error}")


def connection_instagram(user_credentials: dict = {}) -> object:
    """
    The connection with the instagram api is generated (instagram_private_api module)
    Arguments:
        user_credentials (dict) = Dictionary in which the credentials of the user's instagram
                                  account are stored (default {})
    Returns:
            object - The Client object
    """
    
    api = ''
    if not user_credentials:
        credentials = get_credentials()
        username = credentials['instagram']['username']
        password = credentials['instagram']['password']
    else:
        username = user_credentials['username']
        password = user_credentials['password']
    
    settings_file = os.path.abspath('credentials/instagram_api.json')
    
    if os.path.isfile(settings_file):
        delete_cookie(settings_file)
    try:
        if not os.path.isfile(settings_file):
            # If the credentials do not exist, do a new login
            api = Client(
                username, password,
                on_login = lambda x: on_login_callback(x, settings_file))
        else:
            # If the credentials do not exist, do a new login
            try:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook = from_json)
            except Exception as error:
                write_log(STATUS_FILE, str(error), 'Crux')
                print(f"There was an error:{error}")
            
            device_id = cached_settings.get('device_id')
            api = Client(
                username, password,
                device_id = device_id,
                settings = cached_settings)
    
    except ClientLoginError as e:
        write_log(STATUS_FILE, str(e), 'Crux')
        print(e)
    except ClientError as e:
        write_log(STATUS_FILE, e.msg, "Crux")
        print_write_chatbot(
            'ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
    except Exception as e:
        write_log(STATUS_FILE, str(e), "Crux")
    
    print_write_chatbot("You have successfully connected with the instagram! \n", color = 'green',
                        attrs_color = ['bold'])
    
    return api


def connection_aux_api(username: str, password: str) -> object:
    """
    This connection is made specifically for sending messages
    
    Arguments:
        username (str) : The username of the current instagram account
        password (str) : The password of the current instagram account
        
    Returns:
        object
    """
    aux_api = ''
    try:
        logging.disable(logging.CRITICAL)
        aux_api = Bot()
        aux_api.login(username = username, password = password, use_cookie = False)
    
    except Exception as error:
        write_log(STATUS_FILE, str(error), 'Crux')
        print_write_chatbot(f"There was an error:{error}", color = "red", attrs_color = ['bold'])
    
    write_log(STATUS_FILE, "You have successfully connected with the app", 'Crux')
    
    return aux_api
