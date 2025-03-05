# ds_protocol.py

# Starter code for assignment 3 in
# ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME - Jerica Yuan
# EMAIL - jxyuan@uci.edu
# STUDENT ID - 73288143

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple("DataTuple", ["type", "message", "token"])
MessageTuple = namedtuple("MessageTuple", ["type", "message"])

def create_join_request(username: str, password: str) -> str:
    request = {"join": {"username": username, "password": password, "token": ""}}
    return json.dumps(request)


def send_message_request(token: str, recipient: str, message: str, timestamp: str) -> str:
    request = {"token": token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": timestamp}}
    return json.dumps(request)

def direct_message_request(token: str, action:str):
    request = {"token": token, "directmessage": action}
    return json.dumps(request)

def extract_json(json_msg: str) -> DataTuple:
    """
    Call the json.loads function on a json string 
    and convert it to a DataTuple object
    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    """
    try:
        json_obj = json.loads(json_msg)
        response_type = json_obj.get("response", {}).get("type", "error")
        if json_obj.get("response",{}).get("message") is not None:
            message = json_obj.get("response", {}).get("message", "unknown error")
        else:
            message = json_obj.get("response", {}).get("messages", "unknown error")
        token = json_obj.get("response", {}).get("token", None)
        return DataTuple(response_type, message, token)
    except json.JSONDecodeError:
        return DataTuple("error", "Invalid JSON response", None)
