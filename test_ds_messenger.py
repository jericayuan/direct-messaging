# Name: Jerica Yuan
# Email: jxyuan@uci.edu
# ID: 73288143

import pytest
import json
from unittest.mock import patch, MagicMock
from ds_messenger import DirectMessenger, DirectMessage, client_socket
import socket

@pytest.fixture
def mock_socket():
    with patch("ds_messenger.client_socket") as mock:
        mock_conn = MagicMock()
        mock.return_value = mock_conn
        yield mock

@pytest.fixture
def mock_socket_client():
    with patch("socket.socket") as mock:
        mock_conn = MagicMock()
        mock.return_value = mock_conn
        yield mock
        
@pytest.fixture
def messenger():
    return DirectMessenger(dsuserver="testserver", username="testuser", password="testpass")

# testing directmessage get message details 
def test_get_message_details():
    dm = DirectMessage()
    dm.sender = "user1"
    dm.recipient = "user2"
    dm.message = "Hello!"
    dm.timestamp = "2025-02-28T12:35:00"
    
    expected = ("user1", "user2", "Hello!", "2025-02-28T12:35:00")
    assert dm.get_message_details() == expected

# testing directmessenger set and retrieve token function
def test_retrieve_token(messenger):
    assert messenger.retrieve_token() is None
    messenger.set_token("testtoken")
    assert messenger.retrieve_token() == "testtoken"


# testing send functioin
def test_send_success(messenger, mock_socket):
    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_socket.sendall = MagicMock()
    mock_client.recv.return_value = json.dumps({"response": {"type": "ok", "message": "Message sent", "timestamp": ""}}).encode()
    
    messenger.set_token("testtoken")
    success = messenger.send("Hello, world!", "friend123")

    assert success is True
    mock_client.sendall.assert_called()

def test_send_message_failure(messenger, mock_socket):
    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_client.recv.return_value = json.dumps({"response": {"type": "error", "message": "Failed to send", "timestamp": ""}}).encode()
    
    messenger.set_token("testtoken")
    success = messenger.send("Hello, world!", "friend123")
    
    assert success is False


# testing retrieving new message + edge cases
def test_retrieve_new_no_messages(messenger, mock_socket):
    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_response = {
        "response": {
            "type": "ok",
            "messages": [] 
        }
    }
    mock_client.recv.return_value = json.dumps(mock_response).encode()

    messenger.set_token("testtoken")
    messages = messenger.retrieve_new()

    assert messages == [] 

def test_retrieve_new(messenger, mock_socket):
    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_response = {
        "response": {
            "type": "ok",
            "messages": [
                {"from": "user1", "message": "Hi!", "timestamp": "2025-02-28T12:34:56"},
                {"from": "user2", "message": "Hello!", "timestamp": "2025-02-28T12:35:00"}
            ]
        }
    }
    mock_client.recv.return_value = json.dumps(mock_response).encode()
    
    messenger.set_token("testtoken")
    messages = messenger.retrieve_new()
    
    expected_messages = [
        ("user1", "testuser", "Hi!", "2025-02-28T12:34:56"),
        ("user2", "testuser", "Hello!", "2025-02-28T12:35:00")
    ]
    
    assert messages == expected_messages
    mock_client.sendall.assert_called()


# testing retrieve all messages 
def test_retrieve_all(messenger, mock_socket):
    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_response = {
        "response": {
            "type": "ok",
            "messages": [
                {"from": "user1", "message": "Hi!", "timestamp": "2025-02-28T12:34:56"},
                {"from": "user2", "message": "Hello!", "timestamp": "2025-02-28T12:35:00"}
            ]
        }
    }
    mock_client.recv.return_value = json.dumps(mock_response).encode()
    
    messenger.set_token("testtoken")
    messages = messenger.retrieve_all()
    
    expected_messages = [
        ("user1", "testuser", "Hi!", "2025-02-28T12:34:56"),
        ("user2", "testuser", "Hello!", "2025-02-28T12:35:00")
    ]
    
    assert messages == expected_messages
    mock_client.sendall.assert_called()

def test_retrieve_all_no_messages(messenger, mock_socket):
    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_response = {
        "response": {
            "type": "ok",
            "messages": [] 
        }
    }
    mock_client.recv.return_value = json.dumps(mock_response).encode()

    messenger.set_token("testtoken")
    messages = messenger.retrieve_all()

    assert messages == [] 


# testing the client socket
def test_client_socket(messenger, mock_socket_client):
    mock_conn = MagicMock()
    mock_socket_client.return_value  = mock_conn
    join_response = {
        "response": {"type": "ok", "message": "Welcome back!", "token": "testtoken"}
    }
    mock_conn.sendall = MagicMock()
    mock_conn.recv.return_value = json.dumps(join_response).encode()
    client = client_socket('127.0.0.1', 3001, 'asdasd', 'sdfsdf', messenger)
    assert client is not None
    mock_conn.sendall.assert_called()

def test_client_socket_error(messenger, mock_socket_client):
    mock_conn = MagicMock()
    mock_socket_client.return_value = mock_conn
    join_response = {
        "response": {"type": "ok", "message": "Unknown error."}
    }

    mock_conn.sendall = MagicMock()
    mock_conn.recv.return_value = json.dumps(join_response).encode()

    client = client_socket('127.0.0.1', 3001, 'lalala', 'pass', messenger)
    assert client is None
    mock_conn.sendall.assert_called()

def test_client_socket_error_2(messenger, mock_socket_client):
    mock_conn = MagicMock()
    mock_socket_client.return_value = mock_conn
    join_response = {
        "response": {"type": "error", "message": "Unknown error."}
    }

    mock_conn.sendall = MagicMock()
    mock_conn.recv.return_value = json.dumps(join_response).encode()

    client = client_socket('127.0.0.1', 3001, 'testuser', 'testpass', messenger)

    assert client is None

def test_client_socket_exception(messenger):
    client = client_socket('1234', 3001, 'testuser', 'testpass', messenger)

    assert client is None