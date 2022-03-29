import pytest
import json
from src.config import url
import requests
from src.error import InputError, AccessError
from src.helper_functions import generate_jwt
@pytest.fixture
def clear():
    requests.delete(f'{url}clear/v1')
    
def test_user_profile_setemail(clear):
    '''
    Testing for user email updated
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "old@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()
    
    response = requests.put(f'{url}user/profile/setemail/v1', json = {
        'token': user['token'], 
        'email': 'new@gmail.com'})
    
    assert response.status_code == 200

def test_user_profile_setemail_invalid(clear):
    '''
    Testing for user email invalid
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "old@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()
    
    response = requests.put(f'{url}user/profile/setemail/v1', json ={
        'token': user['token'], 
        'email': 'abc.au'})
    assert response.status_code == InputError().code

def test_user_profile_setemail_taken(clear):
    '''
    Testing for user email duplicate
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "email@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()

    response = requests.put(f'{url}user/profile/setemail/v1', json ={
        'token': user['token'], 
        'email': 'email@gmail.com'})
    assert response.status_code == InputError().code
    
def test_user_profile_setemail_token_invalid(clear):
    '''
    Testing for user token invalid
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "email@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()
    token = generate_jwt(user['auth_user_id'] + 1,1)
    response = requests.put(f'{url}user/profile/setemail/v1', json ={
        'token': token, 
        'email': 'new@gmail.com'})
    assert response.status_code == AccessError().code
    
def test_user_profile_sethandle(clear):
    '''
    Testing for user handle updated
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "email@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()
    
    response = requests.put(f'{url}user/profile/sethandle/v1', json = {
        'token': user['token'], 
        'handle_str': 'mynewhandleset'})
    
    assert response.status_code == 200
    
def test_user_sethandle_taken(clear):
    '''
    Testing for user handle taken
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "email@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    
    res = requests.post(f'{url}auth/register/v2', json={
        'email': "adam.smith@ad.unsw.edu.au",
        'password': "password",
        'name_first': "Adam",
        'name_last': "Smith"
    })
    user2 = res.json()
    
    response = requests.put(f'{url}user/profile/sethandle/v1', json = {
        'token': user2['token'], 
        'handle_str': 'haydensmith'})
    
    assert response.status_code == InputError().code
    
def test_user_sethandle_length(clear):
    '''
    Testing for user handle length
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "email@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
        })
    user = res.json()
    
    response = requests.put(f'{url}user/profile/sethandle/v1', json = {
        'token': user['token'], 
        'handle_str': 'hi'})
    
    assert response.status_code == InputError().code
    
    response = requests.put(f'{url}user/profile/sethandle/v1', json = {
        'token': user['token'], 
        'handle_str': 21 * 'A'})
    
    assert response.status_code == InputError().code
