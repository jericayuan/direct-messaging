# Name: Jerica Yuan
# Email: jxyuan@uci.edu
# ID: 73288143

import pytest
import json
from ds_protocol import (
    direct_message_request,
    send_message_request,
    create_join_request,
    extract_json,
    DataTuple
)

def test_create_join_request():
    username = "testuser"
    password = "testpass"
    expected = {"join": {"username": username, "password": password, "token": ""}}
    assert json.loads(create_join_request(username, password)) == expected

def test_send_message_request():
    token = "testtoken"
    recipient = "friend123"
    message = "Hey there!"
    timestamp = "2025-02-28T12:34:56"
    expected = {"token": token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": timestamp}}
    assert json.loads(send_message_request(token, recipient, message, timestamp)) == expected

def test_direct_message_request():
    token = "testtoken"
    action = "new"
    expected = {"token": token, "directmessage": action}
    assert json.loads(direct_message_request(token, action)) == expected

def test_extract_json_valid():
    json_response = json.dumps({
        "response": {"type": "success", "message": "Request completed", "token": "testtoken"}
    })
    expected = DataTuple("success", "Request completed", "testtoken")
    assert extract_json(json_response) == expected

def test_extract_json_valid_with_messages():
    json_response = json.dumps({
        "response": {"type": "success", "messages": "Multiple messages", "token": "testtoken"}
    })
    expected = DataTuple("success", "Multiple messages", "testtoken")
    assert extract_json(json_response) == expected

def test_extract_json_invalid():
    json_response = "invalid json"
    expected = DataTuple("error", "Invalid JSON response", None)
    assert extract_json(json_response) == expected