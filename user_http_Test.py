
'''
pip3 packages
'''
import pytest
import requests
from src import config
import json
from src.error import AccessError, InputError

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


##################################################################################################
# USER_PROFILE (Get)

def test_one_user_profile_v1(clear, jack):
    '''
    test for one user
    '''
    user = jack.json()
    res = requests.get(f'{BASE_URL}user/profile/v1', params={'token': user['token'], 'u_id': user['auth_user_id']})
    assert res.status_code == 200
    assert user['auth_user_id'] == 1

# incorrect token
def test_wrong_token_user_profile_v1(clear, jack):
    '''
    test wrong token
    '''
    user = jack.json()
    res = requests.get(f'{BASE_URL}user/profile/v1', params={'token': 'Wrong', 'u_id': user['auth_user_id']})
    assert res.status_code == AccessError().code

def test_wrong_id_user_profile_v1(clear, jack):
    '''
    test wrong id 
    '''
    user = jack.json()
    res = requests.get(f'{BASE_URL}user/profile/v1', params={'token': user['token'], 'u_id': 'Wrong'})
    assert res.status_code == InputError().code

def test_multiple_user_profile_v1(clear, jack, sarah):
    '''
    test function for multiple users
    '''
    user_1 = jack.json()
    res = requests.get(f'{BASE_URL}user/profile/v1', params={'token': user_1['token'], 'u_id': user_1['auth_user_id']})
    assert res.status_code == 200

##################################################################################################
# USER_PROFILE_SETNAME (Put)

def test_one_user_profile_setname_v1(clear, jack):
    '''
    test profile setname functionality for one user
    '''
    user = jack.json()
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': user['token'], 'name_first': 'new', 'name_last': 'name'})
    assert res.status_code == 200
    assert user['auth_user_id'] == 1

def test_wrong_token_user_profile_setname_v1(clear, jack): 
    '''
    test incorrect token
    '''  
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': 'Wrong', 'name_first': 'new', 'name_last': 'name'})
    assert res.status_code == AccessError().code

def test_multiple_user_profile_setname_v1(clear, jack, sarah):
    '''
    test multiple users
    ''' 
    user1 = jack.json()
    user2 = sarah.json()
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': user1['token'], 'name_first': 'new', 'name_last': 'name'})
    assert res.status_code == 200
    assert user1['auth_user_id'] == 1
    assert user2['auth_user_id'] == 2

def test_user_profile_setname_invalid_first_name_v1(clear, jack):
    '''
    test invalid first name
    '''
    user = jack.json()
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': user['token'], 'name_first': 0*'A', 'name_last': 'name'})
    assert res.status_code == InputError().code
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': user['token'], 'name_first': 51*'A', 'name_last': 'name'})
    assert res.status_code == InputError().code
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': user['token'], 'name_first': '123', 'name_last': 'name'})
    assert res.status_code == InputError().code
def test_user_profile_setname_invalid_last_name_v1(clear, jack):
    '''
    test invalid last name
    '''
    user = jack.json()
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': user['token'], 'name_first': 'new', 'name_last': 0*'A'})
    assert res.status_code == InputError().code
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': user['token'], 'name_first': 'new', 'name_last': 51*'A'})
    assert res.status_code == InputError().code
    res = requests.put(f'{BASE_URL}user/profile/setname/v1', json={'token': user['token'], 'name_first': 'new', 'name_last': '123'})
    assert res.status_code == InputError().code     
