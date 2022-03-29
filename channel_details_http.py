'''
pip3 packages
'''
import pytest
import requests
from src import config
import json
from src.error import AccessError, InputError

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# FIXTURES
@pytest.fixture
def clear():
    return requests.delete(config.url + "clear/v1")

@pytest.fixture
def jack():
    return requests.post(config.url + "auth/register/v2", json={'email':'z5359521@ad.unsw.edu.au', 'password' : 'Pass54321word', 'name_first':'Jack', 'name_last':'Hill'})

@pytest.fixture
def sarah():
    return requests.post(config.url + "auth/register/v2", json={'email':'z5363412@ad.unsw.edu.au', 'password' : 'Parrrpp', 'name_first':'Sarah', 'name_last':'Cat'})

@pytest.fixture
def matt():
    return requests.post(config.url + "auth/register/v2", json={'email':'matt@ad.unsw.edu.au', 'password' : 'Password', 'name_first':'Matt', 'name_last':'Damon'})
    
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# TEST CHANNEL/DETAILS
def test_valid_channel_details(clear, jack):
    '''
    Testing valid channel details
    '''
    user_1 = jack.json()
    response = requests.post(config.url + "channels/create/v2", json = {'token': user_1['token'], 'name': 'jackchannel', 'is_public': True})
    new_channel = response.json()
    response = requests.get(config.url + "channel/details/v2", params = {'token': user_1['token'], 'channel_id': new_channel['channel_id']})
    details = response.json()
    
    assert response.status_code == 200
    assert len(details['owner_members']) == 1
    assert len(details['all_members']) == 1
    
def test_invalid_ch_id_channel_details(clear, jack):
    '''
    Testing invalid channel id
    '''
    user_1 = jack.json()   
    response = requests.get(config.url + "channel/details/v2", params = {'token': user_1['token'], 'channel_id': "-1"}) 
    assert response.status_code == InputError().code
    
def test_invalid_user_not_mem_channel_details(clear, jack, sarah):
    '''
    Testing user is not a member of channel
    '''
    user_1 = jack.json()
    user_2 = sarah.json()
    response = requests.post(config.url + "channels/create/v2", json = {'token': user_1['token'], 'name': 'jackchannel', 'is_public': True})
    new_channel = response.json()
    
    response = requests.get(config.url + "channel/details/v2", params = {'token': user_2['token'], 'channel_id': new_channel['channel_id']}) 
    assert response.status_code == AccessError().code
    
def test_invalid_user_channel_details(clear, jack):
    '''
    Testing user channel details incorrect
    '''
    user_1 = jack.json()
    response = requests.post(config.url + "channels/create/v2", json = {'token': user_1['token'], 'name': 'jackchannel', 'is_public': True})
    new_channel = response.json()
    
    response = requests.get(config.url + "channel/details/v2", params = {'token': "-10000", 'channel_id': new_channel['channel_id']}) 
    assert response.status_code == AccessError().code       
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTING CHANNEL/INVITE
def test_invalid_channel_invite(clear, jack, sarah, matt):
    '''
    Testing invalid channel given
    '''
    user_1 = jack.json()
    user_2 = sarah.json() 

    # invalid channel
    invalid_channel_id = requests.post(config.url + "channel/invite/v2", json = {'token': user_1['token'], 'channel_id': "1000", 'u_id':user_2['auth_user_id']}) 
    assert invalid_channel_id.status_code == InputError().code

def test_invalid_channel_invite_owner(clear, jack, sarah, matt):
    '''
    Testing invalid owner
    '''
    user_1 = jack.json()
    user_2 = sarah.json() 
    response = requests.post(config.url + "channels/create/v2", json = {'token': user_1['token'], 'name': 'jackchannel', 'is_public': True})
    new_channel = response.json()
    # user not owner
    invalid_owner = requests.post(config.url + "channel/invite/v2", json = {'token': "-1", 'channel_id': new_channel['channel_id'], 'u_id': user_2['auth_user_id']}) 
    assert invalid_owner.status_code == AccessError().code
    
def test_invalid_u_id_channel_invite(clear, jack, sarah, matt):
    '''
    Testing invalid u_id
    '''
    user_1 = jack.json()
    response = requests.post(config.url + "channels/create/v2", json = {'token': user_1['token'], 'name': 'jackchannel', 'is_public': True})
    new_channel = response.json()
    # # u_id invalid
    invalid_u_id = requests.post(config.url + "channel/invite/v2", json = {'token': user_1['token'], 'channel_id': new_channel['channel_id'], 'u_id': "1000"})
    assert invalid_u_id.status_code == InputError().code

def test_u_id_already_mem_channel_invite(clear, jack, sarah):
    '''
    Testing when u_id is already member of the channel they are being invited to
    '''
    user_1 = jack.json()
    user_2 = sarah.json() 
    response = requests.post(config.url + "channels/create/v2", json = {'token': user_1['token'], 'name': 'jackchannel', 'is_public': True})
    new_channel = response.json()
    # u_id already mem
    response = requests.post(config.url + "channel/invite/v2", json = {'token': user_1['token'], 'channel_id': new_channel['channel_id'], 'u_id': user_2['auth_user_id']}) 
    u_id_already_mem = requests.post(config.url + "channel/invite/v2", json = {'token': user_1['token'], 'channel_id': new_channel['channel_id'], 'u_id': user_2['auth_user_id']}) 
    assert u_id_already_mem.status_code == InputError().code
    
