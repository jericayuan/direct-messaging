"""
This module provides functions for handling DSU protocol messages,
including:
- Creating join requests
- Sending direct messages
- Extracting JSON responses
"""
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
DataTuple = namedtuple("DataTuple", ["type", "message", "token"])
MessageTuple = namedtuple("MessageTuple", ["type", "message"])


def create_join_request(username: str, password: str) -> str:
    """
    Creates a JSON-formatted join request for the DSU server.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        str: A JSON string containing the join request.
    """
    request = {"join": {
        "username": username,
        "password": password,
        "token": ""}}
    return json.dumps(request)


def send_message_request(
    token: str, recipient: str, message: str, timestamp: str
) -> str:
    """
    Creates a JSON-formatted request to send a direct message.

    Args:
        token (str): The authentication token for the user.
        recipient (str): The recipient's username.
        message (str): The message content.
        timestamp (str): The timestamp of the message.

    Returns:
        str: A JSON string containing the message request.
    """
    request = {
        "token": token,
        "directmessage": {
            "entry": message,
            "recipient": recipient,
            "timestamp": timestamp,
        },
    }
    return json.dumps(request)


def direct_message_request(token: str, action: str):
    """
    Creates a JSON-formatted request to retrieve direct messages.

    Args:
        token (str): The authentication token for the user.
        action (str): The type of message retrieval ("new" or "all").

    Returns:
        str: A JSON string containing the direct message request.
    """
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
        if json_obj.get("response", {}).get("message") is not None:
            message = json_obj.get("response", {}).get("message", "unknown")
        else:
            message = json_obj.get("response", {}).get("messages", "unknown")
        token = json_obj.get("response", {}).get("token", None)
        return DataTuple(response_type, message, token)
    except json.JSONDecodeError:
        return DataTuple("error", "Invalid JSON response", None)
