from urllib import response
import pytest
import json
from src.config import url
import requests
from src.error import AccessError, InputError
from src.helper_functions import generate_jwt

SECRET = 'H15ABADGER'

@pytest.fixture
def clear():
    requests.delete(f'{url}clear/v1')
#################ADMIN_REMOVE#############################
def test_admin_user_remove_invalid_token(clear):
    '''
    Testing for invalid token from admin
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()
    invalid_token = generate_jwt(user['auth_user_id'] + 1,1)
    response = requests.delete(f'{url}admin/user/remove/v1', json = {
        'token' : invalid_token,
        'u_id' : user['auth_user_id']
    })
    assert response.status_code == AccessError().code

def test_admin_user_remove_invalid_id(clear):
    '''
    Testing for invalid id from admin
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()
    
    response = requests.delete(f'{url}admin/user/remove/v1', json = {
        'token' : user['token'],
        'u_id' : user['auth_user_id'] + 100
    })
    assert response.status_code == InputError().code

def test_admin_remove_global_owner(clear):
    '''
    Testing if a user is global owner and being removed
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()

    response = requests.delete(f'{url}admin/user/remove/v1', json = {
        'token' : user['token'],
        'u_id' : user['auth_user_id']
    })
    assert response.status_code == InputError().code
    
def test_admin_not_global_owner(clear):
    '''
    Testing if a user is calling the remove function but is not an owner
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "owner@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user1 = res.json() 
    
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "second@gmail.com",
        'password': "mynameis8",
        'name_first': "John",
        'name_last': "Smith"
    })
    user2 = res.json()
    
    response = requests.delete(f'{url}admin/user/remove/v1', json = {
        'token' : user2['token'],
        'u_id' : user1['auth_user_id']
    })
    assert response.status_code == AccessError().code
    
def test_admin_remove(clear):
    '''
    Testing if admin function works 
    '''
    r = requests.post(f'{url}auth/register/v2', json={
        'email':'hello@gmail.com',
        'password':'password', 
        'name_first':'Hayden', 
        'name_last':'Smith'})
    user1 = r.json()
    
    r = requests.post(f'{url}auth/register/v2', json={
        'email':'goodbye@gmail.com',
        'password':'mynameis8!', 
        'name_first':'John', 
        'name_last':'Smith'})
    user2 = r.json()
    
    response = requests.delete(f'{url}admin/user/remove/v1', json={
        'token': user1['token'], 
        'u_id': user2['auth_user_id']})
    
    assert response.status_code == 200
    
    
    #################ADMIN_USERPERMISSION#############################
def test_admin_userpermission_change_invalid_token(clear):
    '''
    Testing for invalid token
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()
    invalid_token = generate_jwt(user['auth_user_id'] + 1,1)
    
    response = requests.post(f'{url}admin/userpermission/change/v1', json = {
    'token': invalid_token, 
    'u_id':user['auth_user_id'], 
    'permission_id': 1})
    assert response.status_code == AccessError().code

def test_admin_userpermission_change_invalid_id(clear):
    '''
    Testing for invalid id
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user1 = res.json()
    
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "goodbye@gmail.com",
        'password': "mynameis8",
        'name_first': "John",
        'name_last': "Smith"
    })
    user2 = res.json()
    
    response = requests.post(f'{url}admin/userpermission/change/v1', json={
    'token': user1['token'], 
    'u_id':user2['auth_user_id'] + 10, 
    'permission_id': 1
    })
    assert response.status_code == InputError().code

def test_admin_userpermission_invalid_permID(clear):
    '''
    Testing for invalid permission ID
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user1 = res.json()
    
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "goodbye@gmail.com",
        'password': "mynameis8",
        'name_first': "John",
        'name_last': "Smith"
    })
    user2 = res.json()
    
    response = requests.post(f'{url}admin/userpermission/change/v1', json={
    'token': user1['token'], 
    'u_id':user2['auth_user_id'], 
    'permission_id': -1
    })
    assert response.status_code == InputError().code
    
def test_already_permission_level(clear):
    '''
    Testing if user already has the same permission level
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user1 = res.json()
    
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "goodbye@gmail.com",
        'password': "mynameis8",
        'name_first': "John",
        'name_last': "Smith"
    })
    user2 = res.json()
    
    response = requests.post(f'{url}admin/userpermission/change/v1', json = {
    'token': user1['token'], 
    'u_id':user2['auth_user_id'], 
    'permission_id': 2})
    
    assert response.status_code == InputError().code
    
def test_demoted_global_user(clear):
    '''
    Testing if a global user is demoted
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user = res.json()
    
    response = requests.post(f'{url}admin/userpermission/change/v1', json = {
    'token': user['token'], 
    'u_id':user['auth_user_id'], 
    'permission_id': 2})
    
    assert response.status_code == InputError().code

def test_valid_userpermission_change(clear):
    '''
    Testing for a valid success using user permission function
    '''
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    user1 = res.json()
    
    res = requests.post(f'{url}auth/register/v2', json = {
        'email': "goodbye@gmail.com",
        'password': "mynameis8",
        'name_first': "John",
        'name_last': "Smith"
    })
    user2 = res.json()
    
    response= requests.post(f'{url}admin/userpermission/change/v1', json={
    'token': user1['token'], 
    'u_id':user2['auth_user_id'], 
    'permission_id': 1})
    assert response.status_code == 200
