# import imp
from src.helper_functions import check_valid_channel_id , check_auth_user_member_channel, channel_id_to_name, decode_jwt, check_token_valid, check_valid_user_using_auth_user_id, check_auth_user_owner_perms, check_token_owner_perms, check_valid_u_id
from src.data_store import data_store
from src.error import InputError, AccessError

def channel_invite_v2(token, channel_id, u_id):
    '''
    Invites a user with ID u_id to join a channel with ID channel_id. 
    Once invited, the user is added to the channel immediately. 
    In both public and private channels, all members are able to invite users.
    
    Parameters:{ token, channel_id, u_id }
    Return Type:{}
    
    InputError when any of:
      
        - channel_id does not refer to a valid channel
        - u_id does not refer to a valid user
        - u_id refers to a user who is already a member of the channel
      
      AccessError when:
      
        - channel_id is valid and the authorised user is not a member of the channel
    '''
    token_data = decode_jwt(token)
    
    # check if channel is valid
    if check_valid_channel_id(channel_id) == False:
        raise InputError('Error: Channel ID provided is invalid')
    
    # check if invitee is valid
    if check_token_valid(token) == False:
        raise InputError('Error: auth_user_id provided is invalid')
    
    # check if user is valid
    if check_valid_user_using_auth_user_id(u_id) == False:
        raise InputError('Error: u_id provided is invalid')
            
    # check is user is member of channel
    if check_auth_user_member_channel(u_id, channel_id) == True:
        raise InputError('Error: u_id is already a member of the channel')
    
    # check if invitee is member of channel
    if check_auth_user_member_channel(token_data['auth_user_id'], channel_id) == False:
        raise AccessError('Error: auth_user_id is not a member of the channel')
    
    store = data_store.get()
    
    for channel in store['channels']:
        if channel["channel_id"] == channel_id:
            for users in store['users']:
                if users['auth_user_id'] == u_id:
                    channel['all_members'].append(
                        {
                            'u_id': u_id, 
                            'name_first': users['name_first'], 
                            'name_last': users['name_last']
                        }
                    )
    
    return {
    }

def channel_details_v2(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, 
    provide basic details about the channel.
    
    Parameters:{ token, channel_id }
    Return Type:{ name, is_public, owner_members, all_members }
    
    InputError when:
      
        - channel_id does not refer to a valid channel
      
      AccessError when:
      
        - channel_id is valid and the authorised user is not a member of the channel
    '''
    token_data = decode_jwt(token)
    
    # check if channel is valid
    if check_valid_channel_id(channel_id) == False:
        raise InputError('Error: Channel ID provided is invalid')
    
    # check if user is valid
    if check_token_valid(token) == False:
        raise AccessError('Error: User ID provided is invalid')
    
    # check if auth user is member of specified channel
    if check_auth_user_member_channel(token_data['auth_user_id'], channel_id) == False:
        raise AccessError('Error: User is not member of channel')
    
    store = data_store.get()
       
    for channels in store['channels']:
        if channels['channel_id'] == channel_id:         
            return {
                'name': channels['name'],
                'is_public': channels['is_public'], 
                'owner_members': channels['owner_members'],
                'all_members': channels['all_members'],
            }
    
def channel_messages_v2(token, channel_id, start):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, return up to 50 messages between index "start" and "start + 50". 
    Message with index 0 is the most recent message in the channel. 
    This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, 
    returns -1 in "end" to indicate there are no more messages to load after this return.
    
    Parameters:{ token, channel_id, start }
    Return Type:{ messages, start, end }
    
    InputError when:
      
        - channel_id does not refer to a valid channel
        - start greater than total number of messages in channel
      
      AccessError when:
      
        - channel_id is valid and the authorised user is not a member of the channel
    '''
    token_data = decode_jwt(token)
    
    # check if user is valid
    if check_token_valid(token) == False:
        raise AccessError('Error: User ID provided is invalid')

    # check if channel is valid
    if check_valid_channel_id(channel_id) == False:
        raise InputError('Error: Channel ID provided is invalid')

    # check if user is member of specified channel
    if check_auth_user_member_channel(token_data['auth_user_id'], channel_id) == False:
        raise AccessError('Error: Authorised user is not a member of channel with channel_id')

    # get list of messages and length of messages
    store = data_store.get()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            num_messages = len(list(channel['messages']))

    # if there are no messages and start is 0
    if num_messages == 0 and start == 0:
        return {
            'messages': [],
            'start': start,
            'end': -1
        }

    # if start is greater than number of messages
    if start >= num_messages:
        raise InputError('Error: Start is larger than number of messages')

    end_messages = start + 50
    iterator = 0
    msgs = []

    while iterator < 50:
        index = start + iterator
        if index >= end_messages or index >= num_messages:
            break
        # new message 
        channel = channel_id_to_name(channel_id)
        for message in channel['messages']:
            new_message= {
                'message_id': message['message_id'],
                'u_id': message['u_id'],
                'message': message('message'),
                'time_created': message('time_created'),
            }
        
        # append the new message
        msgs.append(new_message)
        iterator = iterator + 1

        if iterator < 50:
            end_messages = -1

        # return messages, start and end values
        return {
            'messages': msgs,
            'start': start,
            'end': end_messages,
        }

def channel_join_v2(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join, adds them to that channel.
    
    Parameters:{ token, channel_id }
    Return Type:{ }
    
    InputError when:
      
        - channel_id does not refer to a valid channel
        - authorised user is already a member of the channel
      
      AccessError when:
      
        - channel_id refers to channel that is private and the authorised user is not a member of the channel and not a global owner
    '''
    token_data = decode_jwt(token)
    # check if user is valid
    if check_token_valid(token) == False:
        raise AccessError('Error: User ID provided is invalid')
    
    # if channel is invalid
    if check_valid_channel_id(channel_id) == False:
        raise InputError('Error: Channel ID provided is invalid')
    
    # check if user is member of specified channel
    if check_auth_user_member_channel(token_data['auth_user_id'], channel_id) == True:
        raise InputError('Error: The user is already part of specified channel')
    
    # grab all of person's detail
    store = data_store.get()
    person = {}
    for user in store['users']:
        if user['auth_user_id'] == token_data['auth_user_id']:
            person = {
                'u_id': user['auth_user_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                # 'permission_id': user['permission_id'],
            }
    
    
    person_data = []
      
    for channel in store['channels']:
        person_data = {
            'name': channel['name'],
            'is_public': channel['is_public'],
        }
        
    if person_data['is_public'] == True or token_data['auth_user_id'] == 1:
        for channel in store['channels']:
            # valid channel ID
            if channel['channel_id'] == channel_id:
                # add person and their detail to channel
                channel['all_members'].append(person)
    else:
        raise AccessError('Error: Channel is private')
    
    
    return {}


def channel_leave_v1(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, remove them as a member of the channel. 
    Their messages should remain in the channel. If the only channel owner leaves, the channel will remain.
        
        Parameters:{token, channel_id}
        
        Return Type:{}
    '''
    token_details = decode_jwt(token)
    auth_user_id = token_details['auth_user_id']

    # check if channel is valid
    if check_valid_channel_id(channel_id) == False:
        raise InputError('Error: Channel ID provided is invalid')
    
    # check if user is valid
    if check_token_valid(token) == False:
        raise InputError('Error: auth_user_id provided is invalid')

    # check if user is a member of the channel
    if check_auth_user_member_channel(auth_user_id, channel_id) == False:
        raise AccessError('Error: User is not a member of the specified channel')

    store = data_store.get()
    
    for channel in store['channels']:
        if channel["channel_id"] == channel_id:
            for users in store['users']:
                if users['auth_user_id'] == auth_user_id:
                    channel['all_members'].remove(
                        {
                            'u_id': auth_user_id, 
                            'name_first': users['name_first'], 
                            'name_last': users['name_last']
                        }
                    )
                if users['auth_user_id'] == auth_user_id and len(channel['owner_members']) > 1:
                     channel['owner_members'].remove(
                        {
                            'u_id': auth_user_id, 
                            'name_first': users['name_first'], 
                            'name_last': users['name_last']
                        }
                    )
    
    return {
    }
    
def channel_addowner_v1(token, channel_id, u_id):
    '''
    Make user with user_id u_id an owner of the channel 
    
    Parameters:{ token, channel_id, u_id }
    Return Type:{}
    '''
    # check if channel is valid
    if check_valid_channel_id(channel_id) == False:
        raise InputError('Error: Channel ID provided is invalid')
    
    # check if inviter is valid
    if check_token_valid(token) == False:
        raise InputError('Error: auth_user_id provided is invalid')

    # check if inviter has owner permissions
    if check_token_owner_perms(token, channel_id) == False:
        raise AccessError('Error: User does not have owner permissions in this channel')
    
    # check if user is valid
    #if check_valid_u_id(u_id) == False:
        #raise InputError('Error: u_id provided is invalid')

    # check if user already has owner permissions
    if check_auth_user_owner_perms(u_id, channel_id) == True:
        raise InputError('Error: User is already an owner of the channel')
    
    # check if user is a member of the channel
    if check_auth_user_member_channel(u_id, channel_id) == False:
        raise InputError('Error: User is not a member of the specified channel')
    
    store = data_store.get()
    for channel in store['channels']:
        if channel["channel_id"] == channel_id:
            for users in store['users']:
                if users['auth_user_id'] == u_id:
                    channel['owner_members'].append(
                        {
                            'u_id': u_id, 
                            'name_first': users['name_first'], 
                            'name_last': users['name_last']
                        }
                    )
    
    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    '''
    Remove user with user_id u_id owner permissions of the channel 
    
    Parameters:{ token, channel_id, u_id }
    Return Type:{}
    '''
    channel = channel_id_to_name(channel_id)

    # check if channel is valid
    if check_valid_channel_id(channel_id) == False:
        raise InputError('Error: Channel ID provided is invalid')
    
    # check if invitee is valid
    if check_token_valid(token) == False:
        raise InputError('Error: auth_user_id provided is invalid')

    # check if invitee has owner permissions
    if check_token_owner_perms(token, channel_id) == False:
        raise AccessError('Error: User does not have owner permissions in this channel')
    
    # check if user is valid
    #if check_valid_u_id(u_id) == False:
        #raise InputError('Error: u_id provided is invalid')

    # check if user already has owner permissions
    if check_auth_user_owner_perms(u_id, channel_id) == False:
        raise InputError('Error: User is not an owner of the channel')
    
    # check if user is a member of the channel
    if check_auth_user_member_channel(u_id, channel_id) == False:
        raise InputError('Error: User is not a member of the specified channel')
        
    # check if user u_id is the only owner of the channel
    if len(channel['owner_members']) == 1:
        raise InputError('Error: User is currently the only owner of the channel')

    # store users details
    store = data_store.get()
    for channel in store['channels']:
        if channel["channel_id"] == channel_id:
            for users in store['users']:
                if users['auth_user_id'] == u_id:
                    channel['owner_members'].remove(
                        {
                            'u_id': u_id, 
                            'name_first': users['name_first'], 
                            'name_last': users['name_last']
                        }
                    )
    return {}
