from src.data_store import data_store
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError
from src.other import clear_v1
import pytest

# --------------------------------------------------------------------------------------------------
#TESTING AUTH REGISTER AND AUTH LOGIN

def test_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc', 'password', 'David', 'Choi')
        
def test_register_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au','a1b2c', 'David', 'Choi')

def test_register_invalid_first_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au','a1b2c3', 0*'A', 'Choi')
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au','a1b2c3', 51*'A', 'Choi')
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au','a1b2c3', '123', 'Choi')
        
def test_register_invalid_last_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au','a1b2c3', 'David', 0*'A')
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au','a1b2c3', 'David', 51*'A')
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au','a1b2c3', 'David', '123')        
        
def test_user_duplicate():
    clear_v1()
    auth_register_v2('z5359104@unsw.edu.au', 'password', 'David', 'Choi')
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au', 'password', 'David', 'Choi')
    with pytest.raises(InputError):
        auth_register_v2('z5359104@unsw.edu.au', 'Mynameis8', 'John', 'Hills')
        
def test_valid_register():
    clear_v1()
    user1 = auth_register_v2('z5359104@unsw.edu.au', 'password', 'David', 'Choi')
    user2 =  auth_register_v2('hi@unsw.edu.au', 'password', 'David', 'Choi')
    assert user1 != user2

def test_registered_incorrect_password():
    clear_v1()
    auth_register_v2('z5359104@unsw.edu.au', 'password', 'David', 'Choi')
    with pytest.raises(InputError):
        auth_login_v2('z5359104@unsw.edu.au', 'incorrectpassword')
        

def test_valid_userID():
    clear_v1()
    register_return = auth_register_v2('z5359104@ad.unsw.edu.au', 'password', 'David', 'Choi')
    auth_user_id1 = register_return

    login_return = auth_login_v2('z5359104@ad.unsw.edu.au', 'password')
    auth_user_id2 = login_return
    assert auth_user_id1['auth_user_id'] == auth_user_id2['auth_user_id']
    assert auth_user_id1['token'] != auth_user_id2['token']
 
    register_return2 = auth_register_v2('hello@gmail.com', 'passlolok', 'David', 'Choi')
    auth_user_id3 = register_return2

    login_return2 = auth_login_v2('hello@gmail.com', 'passlolok')
    auth_user_id4 = login_return2
    assert auth_user_id3['auth_user_id'] == auth_user_id4['auth_user_id']
    assert auth_user_id3['token'] != auth_user_id4['token']
    
def test_handle():
    clear_v1()
    store = data_store.get()
    auth_register_v2('blah@email.com', 'password1', 'abc', 'def0')
    auth_register_v2('blah2@email.com', 'password1', 'abc', 'def0')
    auth_register_v2('blah3@email.com', 'password1', 'abc', 'def')
    auth_register_v2('blah4@email.com', 'password1', 'abc', 'def')
    
    for k in store['users']:
        if k['auth_user_id'] == 1:
            assert k['email'] == 'blah@email.com'
            assert k['name_first'] == 'abc'
            assert k['name_last'] == 'def0'
            assert k['handle_str'] == 'abcdef0'
        elif k['auth_user_id'] == 2:
            assert k['email'] == 'blah2@email.com'
            assert k['name_first'] == 'abc'
            assert k['name_last'] == 'def0'
            assert k['handle_str'] == 'abcdef00'
        elif k['auth_user_id'] == 3:
            assert k['email'] == 'blah3@email.com'
            assert k['name_first'] == 'abc'
            assert k['name_last'] == 'def'
            assert k['handle_str'] == 'abcdef'
        elif k['auth_user_id'] == 4:
            assert k['email'] == 'blah4@email.com'
            assert k['name_first'] == 'abc'
            assert k['name_last'] == 'def'
            assert k['handle_str'] == 'abcdef1'
        


