import pytest
import requests
from src import config
import json
from src.error import AccessError, InputError


BASE_URL = config.url

# --------------------------------------------------------------------
# FIXTURES

@pytest.fixture
def clear():
    return requests.delete(f'{BASE_URL}clear/v1')

# Owner of channel
@pytest.fixture
def token_jack():
    response = requests.post(
        f'{BASE_URL}auth/register/v2', json = {'email': "z5359521@ad.unsw.edu.au", 'password': "Pass54321word", 'name_first': "Jack", 'name_last': "Hill"})
    return response.json()

@pytest.fixture
def channel_id_jack(token_jack):
    response = requests.post(
        f'{BASE_URL}channels/create/v2', json = {'token': token_jack['token'], 'name': "jack_channel", 'is_public': True})
    return response.json()

@pytest.fixture
def message_jack(token_jack, channel_id_jack):
    response = requests.get(
        f'{BASE_URL}channel/messages/v2', params = {'token': token_jack['token'], 'channel_id': channel_id_jack['channel_id'], "start": 0})
    return response.json()

@pytest.fixture
def message_id_jack(channel_id_jack, token_jack):
    response = requests.post(
        f'{BASE_URL}message/send/v1', json = {'token': token_jack['token'], 'channel_id': channel_id_jack['channel_id'], 'message': "Hi I am Jack"}
    )
    return response.json()

    

# Second User
@pytest.fixture
def token_sarah():
    response = requests.post(
        f'{BASE_URL}auth/register/v2', json = {'email': "z5363412@ad.unsw.edu.au", 'password': "Parrrpp", 'name_first': "Sarah", 'name_last': "Cat"})
    return response.json()


# Third User
@pytest.fixture
def token_phil():
    response = requests.post(
        f'{BASE_URL}auth/register/v2', json = {'email': "z5363124@ad.unsw.edu.au", 'password': "notamember!", 'name_first': "Phil", 'name_last': "Seed"})
    return response.json()



# TESTS ---------------- Messages_send_v1 ------------------

#  Invalid Token
def test_message_send_invalid_token(clear, token_jack, token_sarah):
      invalid_token = -1
      response = requests.post(f'{BASE_URL}message/send/v1', json = {
          'token': "-1",
          'channel_id': "1",
          'message': "a"
      })
      assert response.status_code == AccessError().code

# channel_id does not refer to valid channel
# fail response assert 400 otherwise 200 for success --> Input Error
def test_message_invalid_channel_id(clear, token_jack, token_sarah, message_jack):
    invalid_id = 10000000
    response = requests.post(f'{BASE_URL}message/send/v1', json = {
        'token': token_jack['token'],
        'channel_id': invalid_id,
        'message': "Jack is my Name"
        # 'message': message_jack['messages']
    })
    assert response.status_code == InputError().code

# Length of message is less than 1 or over 1000 characters --> Input Error
def test_message_send_length_invalid(clear, token_jack, channel_id_jack):
    message = "a"
    for i in range(1001):
        message += f" {i}"
    response = requests.post(f'{BASE_URL}message/send/v1', json = {
        'token': token_jack['token'],
        'channel_id': channel_id_jack['channel_id'],
        'message': message
    })
    assert response.status_code == InputError().code

# Channel ID is valid but auth user is not member of channel --> Access Error

# def test_message_send_invalid_member_channel(clear, token_phil, channel_id_jack, message_jack):
#     response = requests.post(f'{BASE_URL}message/send/v1', json = {
#         'token': token_phil['token'],
#         'channel_id': channel_id_jack['channel_id'],
#         'message': "Jack is my Name"
#     })
#     assert response.status_code == AccessError().code



# # TESTS ---------------- Message/edit/v1 ------------------

#  Invalid Token
def test_message_edit_invalid_token(clear, token_jack, token_sarah):
      invalid_token = -1
      response = requests.put(f'{BASE_URL}message/edit/v1', json = {
          'token': "-1",
          'message_id': "1",
          'message': "a"
      })
      assert response.status_code == AccessError().code

# Length of message is over 1000 characters --> input error
def test_message_edit_invalid_length(clear, token_jack, channel_id_jack):
    message = "a"
    edit = "a"
    for i in range(1001):
        edit += f" {i}"
    response = requests.post(f'{BASE_URL}message/send/v1', json = {'token': token_jack['token'], \
        'channel_id': channel_id_jack['channel_id'], 'message': message})
   
    id = response.json()
    r = requests.put(f'{BASE_URL}message/edit/v1', json = {
        'token': token_jack['token'],
        'message_id' : "1", 
        'message' : edit
    })
    assert r.status_code == InputError().code


# # Message ID does not refer to a valid message within a channel/DM that the auth user has joined --> Input Error

# def test_message_edit_invalid_message_id(clear, token_jack, channel_id_jack, message_id_jack):
#     message = "Hey this is a test for edit"
#     response = requests.put(f'{BASE_URL}message/edit/v1', json = {
#         'token': token_jack['token'],
#         'message_id': "01232322131",
#         'message': message
#     })
#     assert response.status_code == InputError().code

# # when message ID refers to a valid message ID in a joined channel/DM and the message was not sent by the authroised user making this req --> Access Error

# def test_message_edit_not_auth_user(clear, token_jack, channel_id_jack):
#     message = "Hello this is a test for edit"
#     edit = "edit"
#     response = requests.post(f'{BASE_URL}message/send/v1', json = {
#         'token': token_jack['token'],
#         'channel_id': channel_id_jack['channel_id'],
#         'message': message
#     })
#     message_id = response.json()
#     response = requests.post(f'{BASE_URL}auth/logout/v1', json={'token': token_jack['token']})
#     response = requests.put(f'{BASE_URL}message/edit/v1', json = {
#         'token': token_jack['token'],
#         'message_id': message_id['message_id'],
#         'message': edit
#     })
#     assert response.status_code == AccessError().code

# # authorised user does not have permissions in the channel --> Access Error
# def test_message_edit_auth_user_invalid_permission(clear, token_jack, token_sarah, token_phil, channel_id_jack):
#     message = "Hello this is a test for invalid permission"
#     edit = "edit"
#     response = requests.post(f'{BASE_URL}channel/join/v2', json = {
#         'token': token_sarah['token'],
#         'channel_id': channel_id_jack['channel_id']
#     })
#     response = requests.post(f'{BASE_URL}channel/join/v2', json ={
#         'token': token_phil['token'],
#         'channel_id': channel_id_jack['channel_id']
#     })
#     response = requests.post(f'{BASE_URL}message/send/v1', json = {
#         'token': token_sarah['token'],
#         'channel_id': channel_id_jack['channel_id'],
#         'message': message
#     })
#     message_id = response.json()
#     response = requests.put(f'{BASE_URL}message/edit/v1', json = {
#         'token': token_phil['token'],
#         'message_id': message_id['message_id'],
#         'message': edit
#     })
#     assert response.status_code == AccessError().code


# # TESTS ---------------- Messages/remove/v1 ------------------

# # Invalid Message ID --> Input Error

# def test_message_remove_invalid_message_id(clear, token_jack, channel_id_jack):
#     response = requests.post(f'{BASE_URL}message/send/v1', json = {
#         'token': token_jack['token'],
#         'channel_id': channel_id_jack['channel_id'],
#         'message': "Hi"
#     })
#     response = requests.delete(f'{BASE_URL}message/remove/v1', json = {
#         'token': token_jack['token'],
#         'message_id': "1232313123124421421312123"
#     })
#     assert response.status_code == InputError().code

# # message sent by unauthorised user --> Access Error
# def test_message_remove_invalid_user(clear, token_jack, channel_id_jack):
#     message = "Hello this is a test for remove"
    
#     response = requests.post(f'{BASE_URL}message/send/v1', json = {
#         'token': token_jack['token'],
#         'channel_id': channel_id_jack['channel_id'],
#         'message': message
#     })
#     message_id = response.json()
#     response = requests.post(f'{BASE_URL}auth/logout/v1', json = {'token': token_jack['token']})
#     response = requests.delete(f'{BASE_URL}message/remove/v1', json = {
#         'token': token_jack['token'],
#         'message_id': message_id['message_id']
#     })
#     assert response.status_code == AccessError().code

# # authorised user does not have permissions in the channel --> Access Error
# def test_message_remove_invalid_permission(clear, token_jack, token_sarah, token_phil, channel_id_jack):
#     message = "Hello this is a test for invalid permission"
#     response = requests.post(f'{BASE_URL}channel/join/v2', json = {
#         'token': token_sarah['token'],
#         'channel_id': channel_id_jack['channel_id']
#     })
#     response = requests.post(f'{BASE_URL}channel/join/v2', json = {
#         'token': token_phil['token'],
#         'channel_id': channel_id_jack['channel_id']
#     })
#     response = requests.post(f'{BASE_URL}message/send/v1', json = {
#         'token': token_sarah['token'],
#         'channel_id': channel_id_jack['channel_id'],
#         'message': message
#     })
#     message_id = response.json()
#     response = requests.delete(f'{BASE_URL}message/remove/v1', json = {
#         'token': token_phil['token'],
#         'message_id': message_id['message_id']
#     })
#     assert response.status_code == AccessError().code

def test_message_remove_invalid_token(clear, token_jack, token_sarah):
      invalid_token = -1
      response = requests.delete(f'{BASE_URL}message/remove/v1', json = {
          'token': "-1",
          'message_id': "1"
      })
      assert response.status_code == AccessError().code


















