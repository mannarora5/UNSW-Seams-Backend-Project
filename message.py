from src.error import AccessError, InputError
from src.helper_functions import check_valid_channel_id, check_valid_user_id, u_id_to_handle, check_token_valid, decode_jwt, is_auth_, check_auth_user_member_channel, check_message_id, check_auth_user_owner_perms
from src.data_store import data_store
from time import time
import jwt

def message_send_v1(token, channel_id, message):    
    store = data_store.get()
    # Obtain auth_user_id
    token_details = decode_jwt(token)
    u_id = token_details['auth_user_id']

   

    if check_token_valid(token) == False:
        raise AccessError('Error: Token provided is invalid')

    if check_valid_channel_id(channel_id) == 0:
        raise InputError('Error: Invalid Channel ID')

    if check_valid_channel_id(channel_id) == 1:
        if check_auth_user_member_channel(u_id, channel_id) == False:
            raise AccessError('Error: Not member of channel')
    
    if check_auth_user_owner_perms(u_id, channel_id) == False:
        raise AccessError().code

     
    
    if len(message) > 1000:
        raise InputError('Error: Message is greater than 1000 characters')

    store['message_num'] += 1

    for channel in store['channels']:
        if channel_id == channel['channel_id']:
            u_ids = [channel['all_members'][c]['u_id'] for c in range(len(channel['all_members']))]
            if u_ids not in u_id:
                raise AccessError('Error: Authorised User has not joined the channel they are sending to')

           
            channel['messages'].append ({
                'message_id': store['message_num'],
                'u_id': u_id,
                'message': message,
                'time_created': int(time())

            })

    return {
        'message_id': store['message_num'],
    }


def message_remove_v1(token, message_id):
    store = data_store.get()
    
    if check_token_valid(token) == False:
        raise AccessError('Error: Token provided is invalid')

    
    
    token_details = decode_jwt(token)
    u_id = token_details['auth_user_id']
    if is_auth_(u_id) == False:
        raise AccessError('Error: Not allowed to remove this message as you are unauthorised')
    
    for channel in store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                owners = channel['owner_members']
                for owner in owners:
                    if u_id == owner['u_id']:
                        
                        channel['messages'].remove(message)
                    # Check if the user trying to delete is the one who sent it
                    elif u_id == message['u_id']:
                        
                        channel['messages'].remove(message)

    return()


def message_edit_v1(token, message_id, message):
    store = data_store.get()
    if check_token_valid(token) == False:
        raise AccessError('Error: Token provided is invalid')
    
    if len(message) > 1000:
        raise InputError('Error: Message is greater than 1000 characters')

    if len(message) == 0:
        message_remove_v1(token, message_id)
        return ()
    
    # if check_message_id(message_id) == False:
    #     raise InputError('Error: Incorrect Message ID')


    edit = message
    token_details = decode_jwt(token)
    user_id = token_details['auth_user_id']

    message_exists = False
    user_authorised = False

    if is_auth_(user_id):
        user_authorised = True

    

    for channel in store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                message_exists = True
                owners = channel['owner_members']
                # Check if the user trying to delete is a channel owner
                for owner in owners:
                    if user_id == owner['u_id']:
                        user_authorised = True
                        message['message'] = edit
                    # Check if the user trying to delete is the one who sent it
                    elif user_id == message['u_id']:
                        user_authorised = True
                        message['message'] = edit

    

    if user_authorised == False:
        raise AccessError('Error: Not allowed to edit this message as you are unauthorised')
    if message_exists == False:
        raise InputError('Error: Message not found')

    return {}
    
