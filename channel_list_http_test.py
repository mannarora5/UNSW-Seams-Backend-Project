
'''
pip3 packages
'''
import pytest
import requests
from src import config
import json

BASE_URL = config.url

# FIXTURES
@pytest.fixture
def clear():
    return requests.delete(f"{BASE_URL}clear/v1")
@pytest.fixture
def jack():
    return requests.post(f"{BASE_URL}auth/register/v2", json={'email':'z5359521@ad.unsw.edu.au', 'password' : 'Pass54321word', 'name_first':'Jack', 'name_last':'Hill'})
@pytest.fixture
def sarah():
    return requests.post(f"{BASE_URL}auth/register/v2", json={'email':'z5363412@ad.unsw.edu.au', 'password' : 'Parrrpp', 'name_first':'Sarah', 'name_last':'Cat'})

###################################################################################################
# CHANNELS_LISTALL (Get)

def test_one_user_channels_listall_v2(clear, jack):
    '''
    tests one user list
    '''
    clear
    user = jack.json()
    res = requests.post(f'{BASE_URL}channels/create/v2', json={'token': user['token'], 'name': 'test_channel', 'is_public': True})
    assert res.status_code == 200
    res = requests.get(f'{BASE_URL}channels/listall/v2', params={'token': user['token']})
    channel = res.json()
    assert res.status_code == 200
    assert len(channel['channels']) == 1

def test_incorrect_token_channels_listall(clear, jack):
    '''
    tests incorrect token
    '''
    clear
    user = jack.json()
    res = requests.post(f'{BASE_URL}channels/create/v2', json={'token': user['token'], 'name': 'test_channel', 'is_public': True})
    assert res.status_code == 200
    res = requests.get(f'{BASE_URL}channels/listall/v2', params={'token': 'wrong'})
    assert res.status_code == 403

def test_multiple_channels_listall(clear, jack):
    '''
    tests multiple channels made in a list
    '''
    clear
    user = jack.json()
    requests.post(f'{BASE_URL}channels/create/v2', json={'token': user['token'], 'name': 'test_channel_1', 'is_public': True})
    requests.post(f'{BASE_URL}channels/create/v2', json={'token': user['token'], 'name': 'test_channel_2', 'is_public': False})
    requests.post(f'{BASE_URL}channels/create/v2', json={'token': user['token'], 'name': 'test_channel_3', 'is_public': True})
    res = requests.get(f'{BASE_URL}channels/listall/v2', params={'token': user['token']})
    assert res.status_code == 200
    channel = res.json()
    assert len(channel['channels']) == 3

# ################################################################################################
# #TESTING FOR CHANNELS LIST

def test_single_channel_list(clear, jack):
    '''
    test the function works for one channel
    '''
    clear
    user = jack.json()
    res = requests.post(f'{BASE_URL}channels/create/v2', json={'token': user['token'], 'name': 'test_channel', 'is_public': True})
    res = requests.get(f'{BASE_URL}channels/list/v2', params={'token': user['token']})
    assert res.status_code == 200
    channel = res.json()
    assert len(channel['channels']) == 1


def test_incorrect_token_channels_list(clear, jack, sarah):
    '''
    incorrect user token
    '''
    clear
    user = jack.json()
    res = requests.post(f'{BASE_URL}channels/create/v2', json={'token': user['token'], 'name': 'test_channel', 'is_public': True})
    assert res.status_code == 200
    res = requests.get(f'{BASE_URL}channels/list/v2', params={'token': "wrong"})
    assert res.status_code == 403

def test_multiple_channels_list(clear, jack, sarah):
    '''
    test function works for multiple channels and users
    '''
    clear
    user_1 = jack.json()
    user_2 = sarah.json()
    requests.post(f'{BASE_URL}channels/create/v2', json={'token': user_1['token'], 'name': 'test_channel_1', 'is_public': True})
    requests.post(f'{BASE_URL}channels/create/v2', json={'token': user_1['token'], 'name': 'test_channel_2', 'is_public': False})
    requests.post(f'{BASE_URL}channels/create/v2', json={'token': user_2['token'], 'name': 'test_channel_3', 'is_public': True})
    requests.post(f'{BASE_URL}channels/create/v2', json={'token': user_2['token'], 'name': 'test_channel_4', 'is_public': False})
    res = requests.get(f'{BASE_URL}channels/list/v2', params={'token': user_1['token']})
    assert res.status_code == 200
    channel = res.json()
    assert len(channel['channels']) == 2
