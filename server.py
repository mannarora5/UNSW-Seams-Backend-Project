from distutils.log import debug
import sys
import signal
from json import dumps
#from numpy import save
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.other import clear_v1
from src.users import users_all_v1
from src.user import user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1, user_profile_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.channels import channels_create_v2, channels_listall_v2, channels_list_v2
from src.channel import channel_messages_v2, channel_join_v2, channel_details_v2, channel_invite_v2, channel_addowner_v1, channel_leave_v1, channel_removeowner_v1
from src.dm import dm_create_v1, message_senddm_v1, dm_messages_v1, dm_details_v1, dm_remove_v1, dm_leave_v1, dm_list_v1
from src.helper_functions import save_data
from src.message import message_edit_v1, message_send_v1, message_remove_v1

BASE_URL = config.url

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
    
#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps ({'data': data})

@APP.route("/clear/v1", methods = ["DELETE"])
def clear():
    clear_v1()
    save_data()
    return dumps({})

@APP.route("/auth/register/v2", methods = ['POST'])
def auth_register():
    data = request.get_json()
    result = auth_register_v2(data['email'],
                              data['password'],
                              data['name_first'],
                              data['name_last'])
    save_data()
    return dumps(result)

@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    data = request.get_json()
    result = auth_login_v2(data["email"],
                           data["password"])
    save_data()
    return dumps(result)

@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    data = request.get_json()
    token = data['token']
    result = auth_logout_v1(token)
    save_data()
    return dumps(result)

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    data = request.get_json()

    token = data['token']
    name = data['name']
    is_public = data['is_public']
    result = channels_create_v2(token, name, is_public)
    save_data()
    
    return dumps(result)

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    response = channel_details_v2(token, channel_id)
    save_data()
    
    return dumps(response)

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = data['u_id']
    channel_invite_v2(token, channel_id, u_id)

    save_data()

    return dumps({})

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    response = channel_messages_v2(token, channel_id, start)
    save_data()
    return dumps(response)

@APP.route("/channel/join/v2", methods=["POST"])
def channel_join():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    channel_join_v2(token, channel_id)
    save_data()
    return dumps({})

@APP.route("/channels/listall/v2", methods=['GET'])
def listall():
    token = request.args.get('token')
    data = channels_listall_v2(token)
    save_data()
    return dumps(data)

@APP.route("/channels/list/v2", methods=['GET'])
def channel_list():
    token = request.args.get('token')
    data = channels_list_v2(token)
    save_data()
    return dumps(data)

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    channel_leave_v1(token, channel_id)
    save_data()
    return dumps({})

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    channel_addowner_v1(token, channel_id, u_id)
    save_data()
    return dumps({})

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    channel_removeowner_v1(token, channel_id, u_id)
    save_data()
    return dumps({})

@APP.route("/dm/create/v1", methods=["POST"])
def dm_create():
    data = request.get_json()
    token = data['token']
    u_ids = data['u_ids']
    result = dm_create_v1(token, u_ids)
    save_data()
    return dumps(result)   

@APP.route("/dm/list/v1", methods=["GET"])
def dm_list():
    token = request.args.get('token')
    result = dm_list_v1(token)
    save_data()
    return dumps(result) 
    
    
@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    data = request.json()
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))

    data = dm_details_v1(token, dm_id)
    save_data()    
    return dumps(data)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    dm_remove_v1(token, dm_id)
    save_data()
    
    return dumps({})
    
@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    dm_leave_v1(token, dm_id)
    save_data()
    return dumps({})

@APP.route("/message/message_senddm_v1", methods=['POST'])
def senddm():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    message = request.args.get('message')
    data = message_senddm_v1(token, dm_id, message)
    save_data()
    return dumps(data)
    

@APP.route("/message/remove/v1", methods=["DELETE"])
def message_remove():
    """
    Gets user token and message_id from http json and passes it to the
    message_remove_v1 function
    Returns {} (empty dictionary) on success
    """
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    message_remove_v1(token, message_id)
    save_data()
    return dumps({})

@APP.route("/message/edit/v1", methods=["PUT"])
def message_edit():
    """
    Gets user token, message_id and a message from http json and passes it to the
    message_edit_v2 function
    Returns {} (empty dictionary) on success
    """
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    message = data['message']
    message_edit_v1(token, message_id, message)
    save_data()
    return dumps({})

@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    """
    Gets user data from http json and passes it to the
    message_send_v2 function
    Returns {'message_id' : id} on success
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    data = message_send_v1(token, channel_id, message)
    save_data()
    return dumps(data)

@APP.route("/users/all/v1", methods=['GET'])
def user_all():
    token = request.args.get('token')
    data = request.get_json()
    data = users_all_v1(token)
    save_data()
    return dumps(data)

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def profile_sestname1():
    data = request.get_json()
    user_profile_setname_v1(data['token'], 
                            data['name_first'], 
                            data['name_last'])
    save_data()
    return dumps({})

@APP.route("/user/profile/v1", methods=['GET'])
def profile():
    token = request.args.get('token')
    auth_user_id = request.args.get("u_id", type = int)
    result = user_profile_v1(token, auth_user_id)
    save_data()
    return dumps(result)


@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
   
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    response = dm_messages_v1(token, dm_id, start)
    save_data()
    return dumps(response)

#### NO NEED TO MODIFY BELOW THIS POINT

@APP.route("/user/profile/setemail/v1", methods = ["PUT"])
def set_email():
    data = request.get_json()
    result = user_profile_setemail_v1(data['token'], 
                                    data['email'])
    save_data()
    return dumps(result)

@APP.route("/user/profile/sethandle/v1", methods = ["PUT"])
def set_handle():
    data = request.get_json()
    result = user_profile_sethandle_v1(data['token'],
                                    data['handle_str'])
    save_data()
    return dumps(result)

@APP.route("/admin/user/remove/v1", methods = ["DELETE"])
def user_remove():
    data = request.get_json()
    result = admin_user_remove_v1(data['token'],
                                  data['u_id'])
    save_data()
    return dumps(result)

@APP.route("/admin/userpermission/change/v1", methods = ["POST"])
def permission_change():
    data = request.get_json()
    result = admin_userpermission_change_v1(data['token'],
                                  data['u_id'],
                                  data['permission_id'])
    save_data()
    return dumps(result)

#### NO NEED TO MODIFY BELOW THIS POINT
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
