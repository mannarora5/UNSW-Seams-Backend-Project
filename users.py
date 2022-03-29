'''
module for users
'''
from src.error import AccessError
from src.helper_functions import check_token_valid
from src.data_store import data_store

def users_all_v1(token):
    '''
    Returns a list of all users and their associated details.
    Method = GET
    Perameters:
        { token }
    Return Type:
        { users }
    '''
    store = data_store.get()
    # check if user is valid
    if check_token_valid(token) == False:
        raise AccessError('Error: User ID provided is invalid')
    
    user_list = {'users': []}
    for user in store['users']:
        user_list['users'].append({
            'u_id': user['auth_user_id'],
            'email': user['email'],
            'name_first': user['name_first'] ,
            'name_last': user['name_last'],
            "handle_str": user['handle_str'],
            }
        )
    return user_list
    
