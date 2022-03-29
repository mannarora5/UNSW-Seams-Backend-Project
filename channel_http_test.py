'''
pip3 packages
'''
import pytest
'''
local packages
'''
import requests
from src import config
from src.error import AccessError, InputError
import jwt
import json

#FIXTURES
@pytest.fixture
def clear():
    clear_v1 = requests.delete(config.url + 'clear/v1')
    return clear_v1

#Owner of channel
@pytest.fixture
def token_jack():
    response = requests.post(
        config.url + 'auth/register/v2', json = {"email": "z5359521@ad.unsw.edu.au", "password": "Pass54321word", "name_first": "Jack", "name_last": "Hill"})
    return response.json()

@pytest.fixture
def channel_id_jack(token_jack):
    response = requests.post(
        config.url + 'channels/create/v2', json = {"token": token_jack['token'], "name": "jack_channel", "is_public": True})
    return response.json()

#User who is invited
@pytest.fixture
def token_sarah():
    response = requests.post(
        config.url + 'auth/register/v2', json = {"email": "z5363412@ad.unsw.edu.au", "password": "Parrrpp", "name_first": "Sarah", "name_last": "Cat"})
    return response.json()

@pytest.fixture
def invite_sarah(token_jack, channel_id_jack, token_sarah):
    response = requests.post(
        config.url + 'channel/invite/v2', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": token_sarah['auth_user_id']})
    return response.json()

#Not a member of channel
@pytest.fixture
def token_phil():
    response = requests.post(
        config.url + 'auth/register/v2', json = {"email": "z5363124@ad.unsw.edu.au", "password": "notamember!", "name_first": "Phil", "name_last": "Seed"})
    return response.json()

#Only one instance where Phil is considered a member 
@pytest.fixture
def invite_phil(token_jack, channel_id_jack, token_phil):
    response = requests.post(
        config.url + 'channel/invite/v2', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": token_phil['auth_user_id']})
    return response.json()

#TESTING FOR CHANNEL_LEAVE_1
'''
when valid member successfully leaves channel he was in
'''
def test_channel_leave_successful(clear, token_jack, channel_id_jack, token_sarah, invite_sarah):
    response = requests.post(config.url + 'channel/leave/v1', json = {"token": token_sarah['token'], "channel_id": channel_id_jack['channel_id']})
    assert response.status_code == 200

'''
when valid member tries to leave an invalid channel
'''
def test_channel_leave_invalid_channel(clear, token_jack, channel_id_jack, token_sarah):
    response = requests.post(config.url + 'channel/invite/v2', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": token_sarah['auth_user_id']})
    response = requests.post(config.url + 'channel/leave/v1', json= {"token": token_sarah['token'], "channel_id": '-1234'})
    assert response.status_code == InputError().code

'''
when user that is attempting to leave is not a member of the specified channel
'''
def test_channel_leave_invalid_member(clear, token_phil, channel_id_jack):
    response = requests.post(config.url + 'channel/leave/v1', json = {"token": token_phil['token'], "channel_id": channel_id_jack['channel_id']})
    assert response.status_code == AccessError().code

#TESTING FOR CHANNEL_ADDOWNER_V1
'''
successful add owner
'''
def test_addowner_successful(clear, token_jack, token_sarah, invite_sarah, channel_id_jack):
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": token_sarah['auth_user_id']})
    assert response.status_code == 200  
'''
when channel_id is invalid
'''
def test_addowner_invalid_channel(clear, token_jack, token_sarah, invite_sarah):
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token": token_jack['token'], "channel_id": '-1234', "u_id": token_sarah['auth_user_id']})
    assert response.status_code == InputError().code

'''
when u_id is invalid 

****Not a member
'''
def test_addowner_invalid_u_id(clear, token_jack, channel_id_jack):
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": '-1234'})
    assert response.status_code == InputError().code

'''
when u_id referring to a user not that is not member of specified channel
'''
def test_addowner_invalid_member(clear, token_jack, channel_id_jack, token_phil):
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack["channel_id"], "u_id": token_phil['auth_user_id']})
    assert response.status_code == InputError().code

'''
when u_id refers to a user who is already an owner of the channel
'''
def test_addowner_already_owner(clear, token_jack, channel_id_jack):
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": token_jack['auth_user_id']})
    assert response.status_code == InputError().code

'''
when channel_id is valid and the authorised user does not have owner permissions in the channel
'''
def test_addowner_not_owner(clear, token_sarah, channel_id_jack, invite_phil, token_phil):
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token": token_sarah['token'], "channel_id": channel_id_jack["channel_id"], "u_id": token_phil['auth_user_id']})
    assert response.status_code == AccessError().code

#TESTING FOR CHANNEL_REMOVEOWNER_V1
'''
successful remove owner
'''
def test_removeowner_successful(clear, token_jack, token_sarah, invite_sarah, channel_id_jack):
    response = requests.post(config.url + 'channel/addowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": token_sarah['auth_user_id']})
    response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack["channel_id"], "u_id": token_sarah["auth_user_id"]})
    assert response.status_code == 200 

'''
when channel_id is invalid
'''
def test_removeowner_invalid_channel(clear, token_jack, token_sarah, invite_sarah):
    response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token_jack['token'], "channel_id": -1234, "u_id": token_sarah['auth_user_id']})
    assert response.status_code == InputError().code

'''
when u_id is invalid 

***** Not an owner of channel
'''
def test_removeowner_invalid_u_id(clear, token_jack, channel_id_jack):
    response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": '-1234'})
    assert response.status_code == InputError().code

'''
when u_id referring to a user not that is not member of specified channel 

****Not an owner of channel
'''
def test_removeowner_invalid_member(clear, token_jack, channel_id_jack, token_phil):
    response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack["channel_id"], "u_id": token_phil["auth_user_id"]})
    assert response.status_code == InputError().code

'''
u_id refers to a user who is currently the only owner of the channel
'''
def test_removeowner_only_owner(clear, token_jack, channel_id_jack):
    response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token_jack['token'], "channel_id": channel_id_jack['channel_id'], "u_id": token_jack['auth_user_id']})
    assert response.status_code == InputError().code

'''
when channel_id is valid and the authorised user does not have owner permissions in the channel
'''
def test_removeowner_not_owner(clear, token_sarah, channel_id_jack, invite_phil, token_phil):
    response = requests.post(config.url + 'channel/removeowner/v1', json = {"token": token_sarah['token'], "channel_id": channel_id_jack["channel_id"], "u_id": token_phil["auth_user_id"]})
    assert response.status_code == AccessError().code
