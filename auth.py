from src.data_store import data_store
import requests
import json 
import jwt
from src.helper_functions import check_token_valid, decode_jwt, check_valid_user_id
from src.error import InputError, AccessError

def admin_user_remove_v1(token, u_id):
    '''
   <Given a user by their u_id, remove them from the Seams. This means they should be removed from all channels/DMs, 
   and will not be included in the list of users returned by users/all. Seams owners can remove other Seams owners 
   (including the original first owner). Once users are removed, the contents of the messages they sent will be replaced 
   by 'Removed user'. Their profile must still be retrievable with user/profile, however name_first should be 'Removed' 
   and name_last should be 'user'. The user's email and handle should be reusable.>    
    Arguments:
        - token :: [str] - The user's token.
        - u_id :: [int] - List of user ids.
    Exceptions: 
        InputError - Occurs when:
            - u_id does not refer to a valid user
            - u_id refers to a user who is the only global owner
        AccessError - Occurs when:
            - invalid token
            - the authorised user is not a global owner
    Return Value:
        N/A
    '''
    store = data_store.get()
    #Check if valid token
    if not check_token_valid(token):
        raise AccessError(description="Invalid token")
    data = decode_jwt(token) 
    
    #Check if user exist
    if not check_valid_user_id(u_id):
        raise InputError(description = 'User does not exist')
    
    #Check if user calling function is an owner
    for user in store['users']:
        if user['auth_user_id'] == data['auth_user_id']:
            if user['perm_id'] == 2:
                raise AccessError(description="User calling function is not an owner")
            
    #Check if user is the only owner
    owner_counter = 0
    for user in store["users"]:
        if user["auth_user_id"] == u_id:
            for check_others in store["users"]:
                if check_others["perm_id"] == 1:
                    owner_counter += 1
            if user["perm_id"] == 1 and owner_counter == 1:
                raise InputError(description="User being removed is currently the only global owner")

    #Remove User from Channel
    for channel in store["channels"]:
        for owner in channel["owners"]:
            if owner["auth_user_id"] == u_id:
                channel['owners'].remove(owner)              
        for member in channel["members"]:
            if member["auth_user_id"] == u_id:
                channel['members'].remove(member)
        for channel_message in channel["messages"]:
            if channel_message["u_id"] == u_id:
                channel_message["u_id"] = 'Removed User'
                
    #Remove User's Dms
    for dm in store["dms"]:
        for dm_owner in dm["owners"]:
            if dm_owner["auth_user_id"] == u_id:
                dm['owners'].remove(dm_owner)
        for dm_member in dm["members"]:
            if dm_member["auth_user_id"] == u_id:
                dm['members'].remove(dm_member)
        for dm_message in dm["messages"]:
            if dm_message["u_id"] == u_id:
                dm_message['u_id'] = 'Removed User'
                
    #Remove User's Details
    for user in store["users"]:
        if user["auth_user_id"] == u_id:
            user["first_name"] = "Removed"
            user["last_name"] = "user"
            store["removed_users"].append(user)
            store["users"].pop(store["users"].index(user))
            
    data_store.set(store)
    return {}
    
    
def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Given a user by their user ID, set their permissions to new permissions described by permission_id.
    Arguments:
        token :: [str] - The user's token.
        u_id :: [int] - List of user ids.
        permission_id :: [int] - User's permission ID
    Exceptions: 
        InputError - Occurs when:
            - u_id does not refer to a valid user
            - u_id refers to a user who is the only global owner and they are being demoted to a user
            - permission_id is invalid
        AccessError - Occurs when:
        - the authorised user is not a global owner
    Return Value:
        N/A
    '''
    store = data_store.get()
    if not check_token_valid(token):
        raise AccessError(description="Invalid token")
    data = decode_jwt(token) 
    
    #Check if user exist
    if not check_valid_user_id(u_id):
        raise InputError(description = 'User does not exist')
    
    #Check if valid perm_ID
    valid_perm_IDs = [1,2]
    if permission_id not in valid_perm_IDs:
        raise InputError(description = "Invalid permission ID")
    
    #Check if user calling function is an owner
    for user in store['users']:
        if user['auth_user_id'] == data['auth_user_id'] and user['perm_id'] == 2:
            raise AccessError(description="User calling function is not an owner")
    
    #Check if user is the only owner
    owner_counter = 0
    for user in store["users"]:
        if user["auth_user_id"] == u_id:
            for check_others in store["users"]:
                if check_others["perm_id"] == 1:
                    owner_counter += 1
            if user["perm_id"] == 1 and owner_counter == 1:
                raise InputError(description="User being removed is currently the only global owner")
            if user['perm_id'] == permission_id:
                raise InputError(description = 'User already has permission ID')  
        else:
            user['perm_id'] = permission_id
    
    data_store.set(store)
    return{}
    
