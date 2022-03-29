'''
Creates channels and makes lists of channels
'''
from src.error import InputError, AccessError
from src.helper_functions import check_valid_user_id, get_num_channels, check_token_valid, decode_jwt
from src.data_store import data_store

def channels_list_v2(token):
    '''
    Provide a list of all channels (and their associated details)
    that the authorised user is part of.
    Parameters:{token}
    Return Type:{channels}
    '''
    store = data_store.get()
    
    # check if user is valid
    if check_token_valid(token) == False:
        raise AccessError('Error: User ID provided is invalid')
    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id']
    
    channel_list = {
        'channels': []
    }
    for channel in store['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                channel_list['channels'].append({
                    'channel_id': channel['channel_id'],
                    'name': channel['name']      
                })
    return channel_list

def channels_listall_v2(token):
    '''
    Provide a list of all channels, including private channels, 
    (and their associated details)
    Parameters:{token}
    Return Type:{ channels }
    '''
    store = data_store.get()
    # check if user is valid
    if check_token_valid(token) == False:
        raise AccessError('Error: User ID provided is invalid')
    
    channel_list = {'channels': []}
    for channel in store['channels']:
        channel_list['channels'].append({
            'channel_id': channel['channel_id'],
            'name': channel['name']        
        })
    return channel_list



def channels_create_v2(token, name, is_public):
    '''
    Verifies if parameters input are valid and outputs a channel id 
    Parameters: {token, name, is_public}
    Output: {channel_id}
    '''
    auth_user = decode_jwt(token)    
    # check if token is valid
    
    if check_token_valid(token) == False:
        raise AccessError('Error: Token provided is invalid')
        
    #check if name is valid 
    if len(name) > 20: 
        raise InputError("Error: Length of name must be between 1 and 20 characters.")
    
    if len(name) < 1: 
        raise InputError("Error: Length of name must be between 1 and 20 characters.")    

    #store user's details if valid user
    # user_details = {}
    store = data_store.get()
    for users in store['users']:
        if users['auth_user_id'] == auth_user['auth_user_id']:
            user_details = {
                'auth_user_id': users['auth_user_id'],
                'email': users['email'],
                'password': users['password'],
                'name_first': users['name_first'],
                'name_last': users['name_last'],
                'handle_str': users['handle_str']
            }
            
    #obtain channel id (number of channels)
    num_channels = get_num_channels() + 1
    #create a new channel
    new_channel = {
        "name": name,
        "channel_id": num_channels,
        "is_public": is_public,
        "owner_members": [],
        "all_members": [],
        "messages": [],
    }    
    
    new_channel['owner_members'].append(
        {
        'u_id': user_details['auth_user_id'], 
        'name_first': user_details['name_first'], 
        'name_last': user_details['name_last']
        }
    )
    
    new_channel['all_members'].append(
        {
        'u_id': user_details['auth_user_id'], 
        'name_first': user_details['name_first'],
        'name_last': user_details['name_last']
        }
    )

    #add newly created channel to existing dictionary of channels
    store['channels'].append(new_channel)
    return {'channel_id': num_channels}
