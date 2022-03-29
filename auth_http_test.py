import re
from urllib import response
import pytest
import json
from src.config import url
import requests
from src.error import AccessError, InputError

# --------------------------------------------------------------------------------------------------
#TESTING AUTH REGISTER AND AUTH LOGIN
@pytest.fixture
def clear():
    requests.delete(f'{url}/clear/v1')
    
def test_register_invalid_email(clear):
    '''
    Testing for invalid email
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "abc",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    assert res.status_code == InputError().code
        
def test_register_invalid_password(clear):
    '''
    Testing for invalid password
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "hello@gmail.com",
        'password': "abc",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    assert res.status_code == InputError().code

def test_register_invalid_first_name_min(clear):
    '''
    Testing for minimum first name
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': 0 * "A",
        'name_last': "Smith"
    })
    assert res.status_code == InputError().code

def test_register_invalid_first_name_max(clear):
    '''
    Testing for maximum first name
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': 51 * "A",
        'name_last': "Smith"
    })
    assert res.status_code == InputError().code
    
def test_register_invalid_last_name_max(clear):
    '''
    Testing for maximum last name
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': 51 * "A"
    })
    assert res.status_code == InputError().code 
    
def test_register_invalid_last_name_min(clear):
    '''
    Testing for minimum last name
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': 0 * "A"
    })
    assert res.status_code == InputError().code     
        
def test_user_duplicate(clear):
    '''
    Testing for user duplicate
    '''
    requests.post(f'{url}/auth/register/v2', json={
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"
    })
    assert res.status_code == InputError().code

def test_valid_register(clear):
    '''
    Testing for a valid regsiter
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "bye@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"})
    user1 = res.json()
    
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "john@gmail.com", 
        'password': "password",
        'name_first': "John",
        'name_last': "Smith"})
    user2 = res.json()
    
    assert res.status_code == 200
    assert user1['auth_user_id'] == 1 and user2['auth_user_id'] == 2
    
def test_invalid_email_login(clear):
    '''
    Testing for invalid email login
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "bye@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"})
    res.json()
    
    response = requests.post(f'{url}/auth/login/v2', json={
        'email' : 'wrongemail@gmail.com',
        'password' : 'password'
    })
    assert response.status_code == InputError().code

def test_incorrect_password(clear):
    '''
    Testing for incorrect password
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "bye@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"})
    res.json()
    
    response = requests.post(f'{url}/auth/login/v2', json = {
        'email' : 'wrongemail@gmail.com',
        'password' : 'mynameis8'
    })
    assert response.status_code == InputError().code

def test_auth_login(clear):
    '''
    Testing for user log in
    '''
    res = requests.post(f'{url}/auth/register/v2', json={
        'email': "hello@gmail.com",
        'password': "password",
        'name_first': "Hayden",
        'name_last': "Smith"})
    rego_response = res.json()
    
    res = requests.post(f'{url}/auth/login/v2', json = {
        'email' : 'hello@gmail.com',
        'password' : 'password'
    })
    login_response = res.json()
    
    assert res.status_code == 200
    assert rego_response['auth_user_id'] == login_response['auth_user_id']
    
