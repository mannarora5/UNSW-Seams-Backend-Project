#from src.data_store import initial_object
from src.data_store import initial_object, data_store
import jwt
import re
from unicodedata import name
from xxlimited import new
from json import dump, load
from os import path

from src.error import AccessError


SECRET = 'H15ABADGER'
RESET_SECRET = 'RESETTIME'

#converts token to user id
def decode_jwt(token):    
    try:
        decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        raise AccessError(description= "Unable to decode token") from None
    return decode

# checks auth user id is valid given u_id
def check_valid_user_using_auth_user_id(auth_user_id):
    store = data_store.get()
    valid_ids = store['users']
    for user in valid_ids:
        if user['auth_user_id'] == auth_user_id:
            return 1
    return 0

# check if u_id is valid
def check_valid_u_id(u_id):
    store = data_store.get()
    valid_ids = store['users']
    for user in valid_ids:
        if user['auth_user_id'] == u_id:
            return 1
        return 0

# check if message_id is valid
def check_message_id(message_id):
    store = data_store.get()
    valid_id = store['messages']
    for id in messages:
        if id['message_id'] == message_id:
            return True 
        return False


# check if token has owner permissions
def check_token_owner_perms(token, channel_id):
    token_data = decode_jwt(token)
    channel = channel_id_to_name(channel_id)
    for member in channel['owner_members']:
        if member['u_id'] == token_data['auth_user_id']:
            return True
    return False

# check if auth user has owner permissions
def check_auth_user_owner_perms(u_id, channel_id):
    channel = channel_id_to_name(channel_id)
    for member in channel['owner_members']:
        if member['u_id'] == u_id:
            return True
    return False


# check if user ID is valid
def check_valid_user_id (auth_user_id):
    store = data_store.get()
    valid_ids = store['users']
    for user in valid_ids:
        if user['auth_user_id'] == auth_user_id:
            return True
    return False

#Checks if token matches user
def check_token_valid(token):
    data = decode_jwt(token)
    if not check_valid_user_id(data['auth_user_id']):
        return False
    user = auth_id_to_user(data["auth_user_id"])
    for session in user["session_id"]:
        if session == data["session_id"]:
            return True
    return False
  
# check if channel ID is valid
def check_valid_channel_id(channel_id):
    store = data_store.get()
    valid_channels = store['channels']
    for channel in valid_channels:
        if channel['channel_id'] == channel_id:
            return 1
    return 0

# check if auth user is member of specified channel
def check_auth_user_member_channel(auth_user_id, channel_id):
    channel = channel_id_to_name(channel_id)
    for member in channel['all_members']:
        if member['u_id'] == auth_user_id:
            return True
    return False
    

# retrieve number of channels stored
def get_num_channels():
    store = data_store.get()
    return len(store['channels'])

# retrieve user's id
def get_auth_id(person):
    return person['auth_user_id']  

def get_email(person):
    return person['email']

# get auth user id
def email_to_auth_id(email):
    store = data_store.get()
    for user in store['users']:
        if user['email'] == email:
            return get_auth_id(user)        
    return False

# get auth user
def auth_id_to_user(auth_user_id):
    store = data_store.get()
    for user in store["users"]:
        if get_auth_id(user) == auth_user_id:
            return user
    return False

# get channel
def channel_id_to_name(channel_id):
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return False
# Generate new session ID
def generate_new_sess_id(user):
    if len(user['session_id']) == 0:
        return 1
    session_id = user['session_id'][-1] + 1
    return session_id

#Generate Token
def generate_jwt(auth_user_id, session_id):
    return jwt.encode({'auth_user_id': auth_user_id, 'session_id': session_id}, SECRET, algorithm ='HS256')

# #Decode Token
# def decode_jwt(encoded):
#     return jwt.decode(encoded, SECRET,  algorithms=['HS256'])  


def save_data():
    store = data_store.get()
    with open("persistance/datastore.json", "w") as FILE:
        dump(store, FILE)

# loads saved json file information into data_store
def load_data():
    if path.exists("persistance/datastore.json"):    
        with open("persistance/datastore.json", "r") as FILE:
            store = load(FILE)
            data_store.set(store)
            

def is_auth_(u_id):
    store = data_store.get()
    for user in store['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == 1:
                return True
            return False
    return False

# get handle
def u_id_to_handle(u_id):
    store = data_store.get()
    for user in store["users"]:
        if get_auth_id(user) == u_id:
            return user['handle_str']
    return False
