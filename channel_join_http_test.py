import pytest
import requests
from src import config
import json
from src.error import AccessError, InputError


BASE_URL = config.url
# --------------------------------------------------------------------
# FIXTURES
# Clear function
@pytest.fixture
def clear():
    return requests.delete(f'{BASE_URL}clear/v1')

# Jack Token
@pytest.fixture
def token_jack():
    response = requests.post(
        f'{BASE_URL}auth/register/v2', json = {'email': "z5359521@ad.unsw.edu.au", 'password': "Pass54321word", 'name_first': "Jack", 'name_last': "Hill"})
    return response.json()

# Jack Channel ID
@pytest.fixture
def channel_id_jack(token_jack):
    response = requests.post(
        f'{BASE_URL}channels/create/v2', json = {'token': token_jack['token'], 'name': "jack_channel", 'is_public': True})
    return response.json()

# Sarah Token
@pytest.fixture
def token_sarah():
    response = requests.post(
        f'{BASE_URL}auth/register/v2', json = {'email': "z5363412@ad.unsw.edu.au", 'password': "Parrrpp", 'name_first': "Sarah", 'name_last': "Cat"})
    return response.json()

# Phil Token
@pytest.fixture
def token_phil():
    response = requests.post(
        f'{BASE_URL}auth/register/v2', json = {'email': "z5363124@ad.unsw.edu.au", 'password': "notamember!", 'name_first': "Phil", 'name_last': "Seed"})
    return response.json()

# ---------------------- TESTS for Channel/Messages/V2 -----------------------

# (1) Test for token is invalid
# (2) Test for registered user not member of channel
# (3) Test for channel_id is invalid
# (4) Test for start is greater than total number of messages in channel

# Access Error
def test_channel_messages_invalid_token(clear, channel_id_jack):
    invalid_token = "-100"
    response = requests.get(f'{BASE_URL}channel/messages/v2', params = {
        'token': invalid_token,
        'channel_id': channel_id_jack['channel_id'],
        'start': 0
    })
    assert response.status_code == AccessError().code

# # Access Error
# def test_channel_messages_invalid_member_channel(clear, channel_id_jack, token_sarah):
#     response = requests.get(f'{BASE_URL}channel/messages/v2', params = {
#         'token': token_sarah['token'],
#         'channel_id': channel_id_jack['channel_id'],
#         'start': 0
#     })
#     assert response.status_code == AccessError().code

# Input Error
def test_channel_messages_invalid_channel_id(clear, token_jack):
    invalid_channel_id = -100
    response = requests.get(f'{BASE_URL}channel/messages/v2', params = {
        'token': token_jack['token'],
        'channel_id': invalid_channel_id,
        'start': 0
    })
    assert response.status_code == InputError().code

# Input error
def test_channel_messages_invalid_start(clear, token_jack, channel_id_jack):
    response = requests.get(f'{BASE_URL}channel/messages/v2', params = {
        'token': token_jack['token'],
        'channel_id': channel_id_jack['channel_id'],
        'start': 50
    })
    assert response.status_code == InputError().code

# ---------------------- TESTS for Channel/Join/V2 -----------------------

# (1) Test for token is invalid - Access
# (2) Test for try joining private channel - Access
# (3) Test for try joining private channel - Input

# Access Error
def test_channel_join_invalid_token(clear, channel_id_jack):
    invalid_token = "-100"
    response = requests.post(f'{BASE_URL}channel/join/v2', json = {
        'token': invalid_token,
        'channel_id': channel_id_jack['channel_id']
    })
    assert response.status_code == AccessError().code

# Access Error
def test_channel_join_private_channel(clear, token_jack, token_sarah):
    response = requests.post(f'{BASE_URL}channels/create/v2', json = {
        'token': token_jack['token'],
        'name': "private_channel",
        'is_public': False
    })
    private = response.json()
    response = requests.post(f'{BASE_URL}channel/join/v2', json = {
        'token': token_sarah['token'],
        'channel_id': private['channel_id']
    })
    assert response.status_code == AccessError().code

def test_channel_join_invalid_channel_id(clear, token_jack):
    invalid_channel_id = -1
    response = requests.post(f'{BASE_URL}channel/join/v2', json = {
        'token': token_jack['token'],
        'channel_id': invalid_channel_id
    })
    assert response.status_code == InputError().code






