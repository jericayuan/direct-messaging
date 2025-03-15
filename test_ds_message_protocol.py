"""
Unit tests for ds_protocol.py functions.

This module tests:
- Creating a join request
- Sending direct messages
- Retrieving direct messages
- Extracting and parsing JSON responses
"""
# Name: Jerica Yuan
# Email: jxyuan@uci.edu
# ID: 73288143

import json
from ds_protocol import (
    direct_message_request,
    send_message_request,
    create_join_request,
    extract_json,
    DataTuple,
)


def test_create_join_request():
    """
    Tests whether `create_join_request` correctly formats a join request.
    """
    username = "testuser"
    password = "testpass"
    expected = {"join": {
        "username": username,
        "password": password,
        "token": ""}}
    assert json.loads(create_join_request(username, password)) == expected


def test_send_message_request():
    """
    Tests whether `send_message_request` correctly formats a message request.
    """
    token = "testtoken"
    recipient = "friend123"
    message = "Hey there!"
    timestamp = "2025-02-28T12:34:56"
    expected = {
        "token": token,
        "directmessage": {
            "entry": message,
            "recipient": recipient,
            "timestamp": timestamp,
        },
    }
    assert (
        json.loads(send_message_request(token, recipient, message, timestamp))
        == expected
    )


def test_direct_message_request():
    """
    Tests whether `direct_message_request` correctly formats
    a request for retrieving messages.
    """
    token = "testtoken"
    action = "new"
    expected = {"token": token, "directmessage": action}
    assert json.loads(direct_message_request(token, action)) == expected


def test_extract_json_valid():
    """
    Tests `extract_json` with a valid JSON response
    containing a success message.
    """
    json_response = json.dumps(
        {
            "response": {
                "type": "success",
                "message": "Request completed",
                "token": "testtoken",
            }
        }
    )
    expected = DataTuple("success", "Request completed", "testtoken")
    assert extract_json(json_response) == expected


def test_extract_json_valid_with_messages():
    """
    Tests `extract_json` with a valid JSON response containing messages.
    """
    json_response = json.dumps(
        {
            "response": {
                "type": "success",
                "messages": "Multiple messages",
                "token": "testtoken",
            }
        }
    )
    expected = DataTuple("success", "Multiple messages", "testtoken")
    assert extract_json(json_response) == expected


def test_extract_json_invalid():
    """
    Tests `extract_json` with an invalid JSON string.
    """
    json_response = "invalid json"
    expected = DataTuple("error", "Invalid JSON response", None)
    assert extract_json(json_response) == expected
