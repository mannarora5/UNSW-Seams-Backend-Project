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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#TESTING FOR CHANNELS_CREATE_V2

#Unsuccessful Tests

#Input Error Expected
def test_channels_create_short_name_(clear, token_jack):
    '''
    Name length less than 1 character (Pub)
    ''' 
    
    response = requests.post(config.url + 'channels/create/v2',  json={"token": token_jack['token'], "name": '', "is_public": True})
    assert response.status_code == InputError().code

def test_channels_create_long_name(clear, token_jack):
    '''
    Name length more than 20 characters (Pub)
    '''
    response = requests.post(config.url + 'channels/create/v2',  json={"token": token_jack['token'], "name": 'namelengthmorethan20chars', "is_public": True})
    assert response.status_code == InputError().code

#Access Error Expected
def test_channels_create_invalid_token(clear):
    '''
    Name length more than 20 characters (Pub)
    '''
    response = requests.post(config.url + 'channels/create/v2',  json={"token": "-1234", "name": 'validname', "is_public": True})
    assert response.status_code == AccessError().code

def test_valid_create(clear, token_jack):
    '''
    working test
    ''' 
    response = requests.post(config.url + 'channels/create/v2',  json={"token": token_jack['token'], "name": 'validname', "is_public": True})
    assert response.status_code == 200
