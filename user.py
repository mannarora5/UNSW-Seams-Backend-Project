'''
Module for user
'''
import json
from src.data_store import data_store
from src.helper_functions import auth_id_to_user, check_token_valid, decode_jwt, get_email, check_valid_u_id
from src.error import InputError, AccessError
import re

def user_profile_setemail_v1(token, email):
    '''
   <Update the authorised user's email address>    
    Arguments:
        - Token :: [str] - The user's token.
        - Email :: [str] - An email address.
    Exceptions: 
        InputError - Occurs when:
            - Email entered is not a valid email.
            - Email address is already being used by another user.
        AccessError - Occurs when:
            - Token is invalid
    Return Value:
        N/A
    '''
    store = data_store.get()
    if not check_token_valid(token):
        raise AccessError(description="Invalid token")
    
    data = decode_jwt(token) 
    for user in store['users']:
        if (user['auth_user_id'] == data['auth_user_id']) and data['session_id'] in user['session_id']:
            # checks email address is not already being used by another user
            for user in store["users"]:
                if get_email(user) == email:
                    raise InputError(description="Email is already taken.")
            # checks email entered is a valid email
            regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            if not (re.fullmatch(regex, email)):
                raise InputError(description = "Invalid Email, Please enter valid email address.")
            user['email'] = email
    data_store.set(store)
    return {}

def user_profile_sethandle_v1(token, handle_str):
    '''
   <Update the authorised user's handle (i.e. display name)>    
    Arguments:
        - Token :: [str] - The user's token.
        - handle_str :: [str] - A user's handle.
    Exceptions: 
        InputError - Occurs when:
            - length of handle_str is not between 3 and 20 characters inclusive.
            - handle_str contains characters that are not alphanumeric.
            - the handle is already used by another user
        AccessError - Occurs when:
            - Token is invalid
    Return Value:
        N/A
    '''
    store = data_store.get()
    
    #Check if token is valid
    if not check_token_valid(token):
        raise AccessError(description="Invalid token")
    data = decode_jwt(token)
    #Checking if handle length is valid
    if not 3 <= len(handle_str) <= 20:
        raise InputError(description = "handle_str is not between 3 and 20 characters inclusive")
    #Checking if handle has duplicates
    for user in store['users']:
        if handle_str == user['handle_str']:                              
            raise InputError(description = "handle_str is already in use")
        if (user['auth_user_id'] == data['auth_user_id']) and data['session_id'] in user['session_id']:
            user['handle_str'] = handle_str
    data_store.set(store)
    return {}


def user_profile_v1(token, u_id):
    '''
    For a valid user, returns information about their user_id, email, first name, last name, and handle
    Method = GET
    Parameters:
        { token, u_id }
    Return Type:
        { user }
    '''
    print('1')
    store = data_store.get()      
    # check if user is valid
    if not check_token_valid(token):
        raise AccessError(description="Invalid token")
    print('2')
    if check_valid_u_id(u_id) == False:
        raise InputError('Error: User ID provided is invalid')
    print('3')    
    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id'] 
    print('4')
    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            userInfo = {
                'user_id': u_id,
                'email': user['email'],
                'name_first': user['name_first'] ,
                'name_last': user['name_last'],
                "handle_str": user['handle_str'],
            }   
        break 
    return userInfo
    
def user_profile_setname_v1(token, name_first, name_last):
    '''
    Update the authorised user's first and last name
    Method = PUT
    Parameters:
        { token, name_first, name_last }
    Return Type:
        {}
    '''
    store = data_store.get()
    
    # check if user is valid
    if check_token_valid(token) == False:
        raise InputError('Error: User ID provided is invalid')
        #Checking if first name is valid
    if len(name_first) < 1 or len(name_first) > 50 or str.isdigit(name_first):
        raise InputError ("Invalid first name")
    #Checking if last name is valid
    if len(name_last) < 1 or len(name_last) > 50 or str.isdigit(name_last):
        raise InputError ("Invalid last name")
    
    token_data = decode_jwt(token)
    auth_user_id = token_data['auth_user_id'] 

    for user in store['users']:
        if user['auth_user_id'] == auth_user_id:
            user['name_first'] = name_first,
            user['name_last'] = name_last
            data_store.set(store)
        break 
    return
