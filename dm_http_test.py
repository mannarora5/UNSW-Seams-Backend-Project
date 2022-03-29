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
# from src.dm import list_dm_v1
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
BASE_URL = config.url
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
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

@pytest.fixture
def matt():
    return requests.post(f"{BASE_URL}auth/register/v2", json={'email':'matt@ad.unsw.edu.au', 'password' : 'Password', 'name_first':'Matt', 'name_last':'Damon'})
    
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTING DM/CREATE

def test_dm_create_invalid_token(clear, jack):
    user1 = jack.json()
    response = requests.post(f"{BASE_URL}dm/create/v1", json={'token': "-1", 'u_ids': "2"})
    assert response.status_code == AccessError().code



# def test_valid_dm_create(clear, jack, sarah):
#     user_1 = jack.json()
#     user_2 = sarah.json()
#     u_id1 = user_1['token']
#     u_id2 = user_2['auth_user_id']
#     response = requests.post(f"{BASE_URL}dm/create/v1", json={'token': u_id1, 'u_id': u_id2})
#     assert response.status_code == 200
#     assert response.json() == {'dm_id': 1}
 
# def test_invalid_dm_create(clear, jack, sarah):
#     '''
#     Invalid dm/create
#     '''
#     user_1 = jack.json()
    

    
#     '''
#     Invalid Member = Input Error
#     '''
#     response = requests.post(f"{BASE_URL}dm/create/v1", json={'token': user_1['token'], 'u_ids': 1000})
#     assert response.status_code == InputError().code
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTING DM/LIST
# def test_valid_dm_list(clear, jack, sarah, matt):
#     user_1 = jack.json()
#     user_2 = sarah.json()
#     user_3 = matt.json()
#     u_id1 = user_1['auth_user_id']
#     u_id2 = user_2['auth_user_id']
#     u_id3 = user_3['auth_user_id']
    
#     r1 = requests.post(f"{BASE_URL}dm/create/v1",  json={'token': user_1['token'], 'u_ids': [u_id2, u_id3]})
#     new_dm = r1.json()
#     r2 = requests.post(f"{BASE_URL}dm/create/v1",  json={'token': user_2['token'], 'u_ids': [u_id1]})
#     new_dm_2 = r2.json()
#     response = requests.get(f"{BASE_URL}dm/list/v1",  params={'token': user_1['token']})
#     assert response.json() == {
#         'dms': [
#         {
#                 'dm_id': new_dm['dm_id'], 
#                 'name': new_dm['dm_name']
#         },
#         {
#                 'dm_id': new_dm_2['dm_id'],
#                 'name': new_dm_2['dm_name']
#         }
#         ],
#     }

# def test_invalid_dm_list(clear, sarah):
#     '''
#     Invalid Token = Access Error
#     '''  
#     response = requests.post(f"{BASE_URL}dm/list/v1", json={'token': -1})
#     assert response.status_code == AccessError().code   
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTING DM/REMOVE
def test_dm_remove_invalid_dm_id(clear, jack, sarah):
    user1 = jack.json()
    user2 = sarah.json()
    invalid_id = 50

    response = requests.post(f'{BASE_URL}dm/create/v1', json = {
        'token': user1['token'],
        'u_ids': user2['auth_user_id']
    })
    response = requests.delete(f'{BASE_URL}dm/remove/v1', json = {
        'token': user1['token'],
        'dm_id': invalid_id
    })
    assert response.status_code == InputError().code

# def test_dm_remove_successful(clear, sarah):
#     user1 = jack.json()
#     user2 = sarah.json()
#     response = requests.post(f'{BASE_URL}dm/create/v1', json = {
#         'token': user1['token'],
#         'u_ids': user2['auth_user_id']
#     })
#     response = requests.delete(f'{BASE_URL}dm/remove/v1', json = {
#         'token': user1['token'],
#         'dm_id': response['dm_id']
#     })
#     assert response.status_code == 200
    
def test_dm_remove_invalid_token(clear, jack, sarah):
    user1 = jack.json()
    user2 = sarah.json()
    invalid_id = 50
    
    response = requests.post(f'{BASE_URL}dm/create/v1', json = {
        'token': user1['token'],
        'u_ids': user2['auth_user_id']
        })
    response = requests.delete(f'{BASE_URL}dm/remove/v1', json = {
        'token': 'wrong',
        'dm_id': invalid_id
    })
    assert response.status_code == AccessError().code

# def test_dm_remove_not_original_owner():
#     user1 = jack.json()
#     user2 = sarah.json()
#     invalid_id = 50
    
#     response = requests.post(f'{BASE_URL}dm/create/v1', json = {
#         'token': user1['token'],
#         'u_ids': user2['auth_user_id']
#     })
#     response = requests.delete(f'{BASE_URL}dm/remove/v1', json = {
#         'token': user2['token'],
#         'dm_id': invalid_id
#     })
#     assert response.status_code == AccessError().code
    
def test_dm_remove_http_unauthorised_user(clear, jack, sarah, matt):
    user1 = jack.json()
    user2 = sarah.json()
    user3 = matt.json()

    valid_start = 0
    response = requests.post(f'{BASE_URL}dm/create/v1', json = {
        'token': user1['token'],
        'u_ids': user2['auth_user_id']
    })
    dm1 = response.json()

    response = requests.delete(f'{BASE_URL}dm/remove/v1', json = {
        'token': user2['token'],
        'dm_id': "1"
    })
    assert response.status_code == InputError().code


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTING DM/DETAILS
# def test_valid_dm_details(clear, jack, sarah):
#     user_1 = jack.json()
#     user_2 = sarah.json()
#     u_id2 = user_2['auth_user_id']
    
#     response = requests.post(f"{BASE_URL}dm/create/v1", json={'token': user_1['token'], 'u_ids': [u_id2]})
#     dm = response.json()
#     response = requests.get(f"{BASE_URL}dm/details/v1", params={'token': user_1['token'], 'dm_id': dm['dm_id']})
#     dm_details = response.json()
    
#     assert dm_details['name'] == "sarahcat, jackhill"
#     assert dm_details['members'] == [{'u_id': 1, 'email': 'z5359521@ad.unsw.edu.au', 'name_first': 'Sarah', 'name_last': 'Cat'},
#                                     {'u_id': 2, 'email': 'z5363412@ad.unsw.edu.au', 'name_first': 'Jack', 'name_last': 'Hill'}]
    
# def test_invalid_dm_details(clear, jack, sarah, matt):
#     user_1 = jack.json()
#     user_2 = sarah.json()
#     user_3 = matt.json()
#     u_id2 = user_2['auth_user_id']
#     response = requests.post(f"{BASE_URL}dm/create/v1", json={'token': user_1['token'], 'u_ids': [u_id2]})
#     dm = response.json()
    
#     '''
#     Invalid Token = Access Error
#     '''  
#     response = requests.get(f"{BASE_URL}dm/create/v1", params={'token': -1, 'dm_id': [u_id2]})
#     assert response.status_code == AccessError().code
    
#     '''
#     Invalid Member = Input Error
#     '''
#     response = requests.get(f"{BASE_URL}dm/create/v1", params={'token': user_1['token'], 'dm_id': 1000})
#     assert response.status_code == InputError().code
    
#     '''
#     User is not member of DM = Access Error
#     '''
#     response = requests.get(f"{BASE_URL}dm/create/v1", params={'token': user_3['token'], 'dm_id': dm['dm_id']})
#     assert response.status_code == AccessError().code
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTING DM/LEAVE
# def test_valid_dm_leave(clear, jack, sarah, matt):
#     user_1 = jack.json()
#     user_2 = sarah.json()
#     user_3 = matt.json()

#     u_id2 = user_2['auth_user_id']
#     u_id3 = user_3['auth_user_id']
    
#     response = requests.post(f"{BASE_URL}dm/create/v1",  json={'token': user_1['token'], 'u_ids': [u_id2, u_id3]})
#     dm = response.json()  
#     response = requests.post(f"{BASE_URL}dm/leave/v1",  json={'token': user_1['token'], 'dm_id': dm[u_id3]})
#     response = requests.get(f"{BASE_URL}dm/details/v1", params={'token': user_1['token'], 'dm_id': dm['dm_id']})
#     dm_details = response.json()
    
#     assert dm_details['name'] == "sarahcat, jackhill"
#     assert dm_details['members'] == [{'u_id': 1, 'email': 'z5359521@ad.unsw.edu.au', 'name_first': 'Sarah', 'name_last': 'Cat'},
#                                     {'u_id': 2, 'email': 'z5363412@ad.unsw.edu.au', 'name_first': 'Jack', 'name_last': 'Hill'}]
    
# def test_invalid_dm_leave(clear, jack, matt, sarah):
#     user_1 = jack.json()
#     user_2 = sarah.json()
#     user_3 = matt.json()
        
#     u_id2 = user_2['auth_user_id']
#     u_id3 = user_3['auth_user_id']
    
#     response = requests.post(f"{BASE_URL}dm/create/v1",  json={'token': user_1['token'], 'u_ids': [u_id2]})
#     dm = response.json()  
    
#     '''
#     Invalid Token = Access Error
#     '''
#     response = requests.post(f"{BASE_URL}dm/leave/v1",  json={'token': -1, 'dm_id': dm[u_id2]})
#     assert response.status_code == AccessError.code
#     '''
#     Invalid DM id = Input Error
#     '''
#     response = requests.post(f"{BASE_URL}dm/leave/v1",  json={'token': user_1['token'], 'dm_id': 1000})
#     assert response.status_code == InputError().code
    
#     '''
#     User is not in DM = Access Error
#     '''
#     response = requests.post(f"{BASE_URL}dm/leave/v1",  json={'token': user_1['token'], 'dm_id': dm[u_id3]})
    
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# -------- TESTS for DM/MESSAGES/V1-----------------------------

def test_dm_messages_invalid_dm_id(clear, jack, sarah):
    user1 = jack.json()
    user2 = sarah.json()
    invalid_id = 50
    valid_start = 0
    response = requests.post(f'{BASE_URL}dm/create/v1', json = {
        'token': user1['token'],
        'u_ids': user2['auth_user_id']
    })
    response = requests.get(f'{BASE_URL}dm/messages/v1', params = {
        'token': user1['token'],
        'dm_id': invalid_id,
        'start': valid_start
    })
    assert response.status_code == InputError().code


# def test_dm_messages_invalid_start(clear, jack, sarah):
#     user1 = jack.json()
#     user2 = sarah.json()
#     invalid_start = 33

#     response = requests.post(f'{BASE_URL}dm/create/v1', json = {
#        'token': user1['token'],
#        'u_ids': user2['auth_user_id']
#     })
#     dm1 = response.json()
#     response = requests.get(f'{BASE_URL}dm/messages/v1', params = {
#        'token': user1['token'],
#        'dm_id': dm1['dm_id'],
#        'start': invalid_start
#     })
#     assert response.status_code == InputError().code

# def test_dm_messages_http_unauthorised_user(clear, jack, sarah, matt):
#     user1 = jack.json()
#     user2 = sarah.json()
#     user3 = matt.json()

#     valid_start = 0
#     response = requests.post(f'{BASE_URL}dm/create/v1', json = {
#         'token': user1['token'],
#         'u_ids': user2['auth_user_id']
#     })
#     dm1 = response.json()

#     response = requests.get(f'{BASE_URL}dm/messages/v1', params = {
#         'token': user3['token'],
#         'dm_id': dm1['dm_id'],
#         'start': valid_start
#     })
#     assert response.status_code == AccessError().code

# --------------TESTS FOR MESSAGE/SEND/DM----------------

# MESSAGE_SENDDM (Post)
# Not sure of this is correct. 
# def test_pass_message_senddm(clear, jack, sarah):
#     user1 = jack.json()
#     user2 = sarah.json()
#     message = requests.get(f'{BASE_URL}dm/create/v1', params={'token': user1['token'], 'u_id': user2['auth_user_id']})
#     res = requests.post(f'{BASE_URL}message/senddm/v1', json={'token': user1['token'], 'dm_id': message['dm_id'], 'message': "test message"})
#     assert res.status_code == 200
#     message = res.json()
#     assert len(message['message_id']) == 1

# def test_invalid_token_message_senddm():
#     user1 = jack.json()
#     user2 = sarah.json()
#     message = requests.get(f'{BASE_URL}dm/create/v1', params={'token': user1['token'], 'u_id': user2['auth_user_id']})
#     res = requests.post(f'{BASE_URL}message/senddm/v1', json = {'token': '', 'dm_id': message['dm_id'], 'message': "test message"})
#     assert res.status_code == InputError().code

# def test_invalid_dm_id_message_senddm():
#     user1 = jack.json()
#     user2 = sarah.json()
#     message = requests.get(f'{BASE_URL}dm/create/v1', params={'token': user1['token'], 'u_id': user2['auth_user_id']})
#     res = requests.post(f'{BASE_URL}message/senddm/v1', json={'token': user1['token'], 'dm_id': '', 'message': "test message"})
#     assert res.status_code == InputError().code

# def test_invalid_message_message_senddm():
#     user1 = jack.json()
#     user2 = sarah.json()
#     message = requests.get(f'{BASE_URL}dm/create/v1', params={'token': user1['token'], 'u_id': user2['auth_user_id']})
#     res = requests.post(f'{BASE_URL}message/senddm/v1', json = {'token': user1['token'], 'dm_id': message['dm_id'], 'message': ''})
#     assert res.status_code == InputError().code

# def test_not_member_of_DM_message_senddm():
#     user1 = jack.json()
#     user2 = sarah.json()
#     user3 = requests.post(f"{BASE_URL}auth/register/v2", json={'email':'z6359521@ad.unsw.edu.au', 'password' : 'Pass54321word', 'name_first':'Harry', 'name_last':'Hat'})
#     message = requests.post(f'{BASE_URL}dm/create/v1', json={'token': user1['token'], 'u_id': user2['auth_user_id']})
#     res = requests.post(f'{BASE_URL}message/senddm/v1', json={'token': user3['token'], 'dm_id': message['dm_id'], 'message': ''})
#     assert res.status_code == AccessError().code
