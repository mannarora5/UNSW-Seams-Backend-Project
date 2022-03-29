from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper_functions import check_token_valid, check_valid_user_using_auth_user_id, decode_jwt, check_valid_user_id, check_valid_user_using_auth_user_id
import jwt
import json


def dm_create_v1(token, u_ids):
    '''
    u_ids contains the user(s) that this DM is directed to, and will not include 
    the creator. The creator is the owner of the DM. name should be automatically 
    generated based on the users that are in this DM. The name should be an 
    alphabetically-sorted, comma-and-space-separated list of user handles, 
    e.g. 'ahandle1, bhandle2, chandle3'.
    
    HTTP METHOD: POST
    Parameters:{ token, u_ids }
    Return Type:{ dm_id }
    
    InputError when any of:    
        - any u_id in u_ids does not refer to a valid user
        - there are duplicate 'u_id's in u_ids
    '''
    store = data_store.get()
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError("Error: invalid token")

    if check_valid_user_id(u_ids): False
        raise InputError('Error Invalid Member')
    # Check if user is valid
    for u_id in u_ids:
        if check_valid_user_using_auth_user_id(u_id) == False:
            raise InputError('Error: u_id provided is invalid')
        
    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id']
    
    # If user ids valid, store details of owner
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            user_details = {
                'u_id' : user['u_id'],
                'email' : user['email'],
                'name_first' : user['name_first'],
                'name_last' : user['name_last'],
                'handle_str' : user['handle_str'],
                'password' : user['password']
            }
    
    # Store handles of members
    dm_name_list = []
    dm_name_list.append(user_details['handle_str'])
    
    for u_id in u_ids:
        for user in store['users']:
            if user['auth_user_id'] == u_id:
                dm_name_list.append(user['handle_str'])
        
    sorted_dm_name_list = sorted(dm_name_list, key=str.lower)
    dm_num = len(store['dms']) + 1
    dm_name = ', '.join(sorted_dm_name_list)
    
    members = []
    members.append(user_details)
    new_dm = {
                'dm_id' : dm_num,
                'name' : dm_name,
                'owner_members' : [],
                'all_members' : [],
                'messages': []
    }
    for user in store['user']:
        if user['auth_user_id'] == auth_user_id:            
            new_dm['owner_members'].append({
                'auth_user_id': auth_user_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str']                
            })
            # append owner to dm members
            new_dm['all_members'].append({
                'u_id': auth_user_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str']
            })
        
    #append all u_ids in dm members
    for u_id in u_ids:
        for user in store['users']:
            if user['auth_user_id'] == u_id:
                new_dm['all_members'].append({
                    'u_id': u_id,
                    'email': user['email'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last'],
                    'handle_str': user['handle_str']
                })

    store['dms'].append(new_dm)
    return {'dm_id': dm_num}        

    
def dm_list_v1(token):
    '''
    Returns the list of DMs that the user is a member of.
    
    HTTP METHOD: GET
    Parameters:{ token }
    Return Type:{ dms }
    '''
    store = data_store.get()
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Error invalid token")
    
    dm_list = {}
    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id']
    for dm in store['dms']:
        for member in dm['all_members']:
            if member['u_id'] == auth_user_id:
                dm_list['dms'].append({
                    'dm_id': dm['dm_id'],
                    'name': dm['name']
                })
    
    return dm_list
    
def dm_remove_v1(token, dm_id):
    '''
    Remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.
    
    HTTP METHOD: DELETE
    Parameters:{ token, dm_id }
    Return Type:{}
    
    AccessError when:
        - dm_id is valid and the authorised user is not the original DM creator
        - dm_id is valid and the authorised user is no longer in the DM
    '''
    store = data_store.get()
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError("Error invalid token")
    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id']

    if check_valid_user_using_auth_user_id(auth_user_id) == 0:



    
    valid_dm = False
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            for member in dm['owner_members']:
                if member['auth_user_id'] == auth_user_id:
                    store['dms'].remove(dm)
        
    if valid_dm == False:
        raise InputError(description="Dm_id does not refer to a valid DM")
    
    return{}
 
def dm_details_v1(token, dm_id):
    '''
    Given a DM with ID dm_id that the authorised user is a member of, provide 
    basic details about the DM.
    
    HTTP METHOD: GET
    Parameters:{ token, dm_id }
    Return Type:{ name, members }
    
    InputError when:      
        - dm_id does not refer to a valid DM
      
    AccessError when:      
        - dm_id is valid and the authorised user is not a member of the DM
    '''
    store = data_store.get()
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Error invalid token")
     
    valid_dm = False
    #if invalid dm_id
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            
    if valid_dm == False:
        raise InputError(description="Dm_id does not refer to a valid DM")
    
    dm_details = {}
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            dm_details['name'] = dm['name']
            dm_details['members'] = []
            for member in dm['all_members']:
                dm_details['members'].append({
                    'u_id': member['u_id'], 
                    'email': member['email'],
                    'name_first': member['name_first'],
                    'name_last': member['name_last'],
                    'handle_str': member['handle_str']          
                })               
        
    return dm_details
        
    
def dm_leave_v1(token, dm_id):
    '''
    Given a DM ID, the user is removed as a member of this DM. The creator is allowed to 
    leave and the DM will still exist if this happens. This does not update the name of 
    the DM.
    
    HTTP METHOD: POST
    Parameters:{ token, dm_id }
    Return Type:{}
    
    InputError when:      
        - dm_id does not refer to a valid DM
      
    AccessError when:
        - dm_id is valid and the authorised user is not a member of the DM
    '''
    store = data_store.get()
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Error invalid token")
    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id']
    
    valid_dm = False
    #if invalid dm_id
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            
    if valid_dm == False:
        raise InputError(description="Dm_id does not refer to a valid DM")
    
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            for member in dm['all_members']:
                if member['u_id'] == auth_user_id:
                    # Copy all the user data for easier access
                    dm['all_members'].remove(member)
                    
    return {}

def message_senddm_v1(token, dm_id, message):
    # Send a message from authorised_user to the DM specified by dm_id. 
    # Note: Each message should have it's own unique ID, 
    # i.e. no messages should share an ID with another message, even if that other message is in a different channel or DM.

    # POST
        
    # Parameters:{ token, dm_id, message }
    # Return Type:{ message_id }

    #   InputError when any of:
    #     dm_id does not refer to a valid DM
    #     length of message is less than 1 or over 1000 characters
    #   AccessError when:
    #     dm_id is valid and the authorised user is not a member of the DM

    store = data_store.get()
    
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Error invalid token")

    # # Check message is valid
    # characters = 0
    # for i in message:
    #     characters = characters + 1
        
    # if characters < 1 | characters > 1000:
    #     raise InputError(description="Error message to long")

    # if user is not a part of the dm 
    valid_user = 0
    valid_dm = 0
    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id']
    for dm in store['dm']:
        for members in dm['all_members']:
            for user in members['u_id']:
                if (user['u_id'] == auth_user_id):
                    valid_user = 1
                    break

    # Check if dm id is valid
    if valid_dm == 0:
        raise InputError('Error invalid dm_id')

    num_messages = 0
    for dm in store['dm']:
        num_messages = num_messages + 1
        for id in dm['dm_id']:
            num_messages = num_messages + 1
            if id == dm_id: 
                valid_dm = 1
                new_message = {
                    'message_id': num_messages,
                    'data': message,
                }

    if valid_dm == 1 & valid_user == 0:
        raise AccessError('Error not a member of DM')
    
    store['dm']['messages'].append(new_message)

    return {new_message['message_id']}


def dm_messages_v1(token, dm_id, start):
    store = data_store.get()
    if check_token_valid(token) == False:
        raise AccessError('Error invalid token')

    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id']
    valid_dm = False
    member_valid = False
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            for member in dm['all_members']:
                if auth_user_id == member['u_id']:
                    member_valid = True
                    break
            messages = dm['messages']
            break

    if valid_dm == False:
        raise InputError('Error: Invalid DM')

    if member_valid == False:
        raise AccessError('Error: Invalid Member for DM')

    if start >= len(messages) or start < 0:
            raise InputError('Error: Invalid Start Value')
    end = start
    output = []
    while end < 50 and end < len(messages):
        output.append(messages[::-end-1])
        end += 1
    if end < 50:
        end = -1
    return {
        'messages': output,
        'start': start,
        'end': end,
    }

      





    


