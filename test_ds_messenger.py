# Name: Jerica Yuan
# Email: jxyuan@uci.edu
# ID: 73288143
"""
Tests the coverage of ds_messenger.py module using
unittest.mock and MagicMock to replicate socket connections.
"""
import json
from unittest.mock import patch, MagicMock
import pytest
from ds_messenger import DirectMessenger, DirectMessage


@pytest.fixture
def mock_socket():
    """Mocks the client socket for DirectMessenger."""

    with patch("ds_messenger.DirectMessenger.client_socket") as mock:
        mock_conn = MagicMock()
        mock.return_value = mock_conn
        yield mock


@pytest.fixture
def mock_socket_client():
    """Mocks the socket.socket function."""

    with patch("socket.socket") as mock:
        mock_conn = MagicMock()
        mock.return_value = mock_conn
        yield mock


@pytest.fixture
def messenger():
    """Creates an instance of DirectMessenger for testing."""

    return DirectMessenger(
        dsuserver="testserver", username="testuser", password="testpass"
    )


def test_get_message_details():
    """Tests the string and representation methods
    of DirectMessage + get message details."""

    dm = DirectMessage()
    dm.sender = "user1"
    dm.recipient = "user2"
    dm.message = "Hello!"
    dm.timestamp = "2025-02-28T12:35:00"

    expected_repr = "DirectMessage(sender='user1', recipient='user2', " \
        "message='Hello!', timestamp='2025-02-28T12:35:00')"
    assert repr(dm) == expected_repr
    expected_str = "[2025-02-28T12:35:00] user1 -> user2: Hello!"
    assert str(dm) == expected_str


# pylint: disable=redefined-outer-name
def test_retrieve_token(messenger):
    """Tests setting and retrieving the authentication token."""

    assert messenger.retrieve_token() is None
    messenger.set_token("testtoken")
    assert messenger.retrieve_token() == "testtoken"
    assert messenger.token == "testtoken"
    assert messenger.dsuserver == "testserver"


# pylint: disable=redefined-outer-name
def test_send_success(messenger, mock_socket):
    """Tests sending a message successfully."""

    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_socket.sendall = MagicMock()
    mock_client.recv.return_value = json.dumps(
        {"response": {
            "type": "ok",
            "message": "Message sent",
            "timestamp": ""}}
    ).encode()

    messenger.set_token("testtoken")
    success = messenger.send("Hello, world!", "friend123")

    assert success is True
    mock_client.sendall.assert_called()


# pylint: disable=redefined-outer-name
def test_send_message_failure(messenger, mock_socket):
    """Tests message sending failure scenario."""

    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_client.recv.return_value = json.dumps(
        {"response": {
            "type": "error",
            "message": "Failed to send",
            "timestamp": ""}}
    ).encode()

    messenger.set_token("testtoken")
    success = messenger.send("Hello, world!", "friend123")

    assert success is False
    mock_client.sendall.assert_called()


# pylint: disable=redefined-outer-name
def test_retrieve_new_no_messages(messenger, mock_socket):
    """Tests retrieving new messages when there are none."""

    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_response = {"response": {"type": "ok", "messages": []}}
    mock_client.recv.return_value = json.dumps(mock_response).encode()

    messenger.set_token("testtoken")
    messages = messenger.retrieve_new()

    assert messages == []


# pylint: disable=redefined-outer-name
def test_retrieve_new(messenger, mock_socket):
    """Tests retrieving new messages from the server."""

    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_response = {
        "response": {
            "type": "ok",
            "messages": [
                {"from": "user1", "message": "Hi!",
                 "timestamp": "2025-02-28T12:34:56"},
                {
                    "from": "user2",
                    "message": "Hello!",
                    "timestamp": "2025-02-28T12:35:00",
                },
            ],
        }
    }
    mock_client.recv.return_value = json.dumps(mock_response).encode()

    messenger.set_token("testtoken")
    messages = messenger.retrieve_new()

    expected_messages = []

    msg1 = DirectMessage()
    msg1.sender = "user1"
    msg1.recipient = "testuser"
    msg1.message = "Hi!"
    msg1.timestamp = "2025-02-28T12:34:56"

    msg2 = DirectMessage()
    msg2.sender = "user2"
    msg2.recipient = "testuser"
    msg2.message = "Hello!"
    msg2.timestamp = "2025-02-28T12:35:00"

    expected_messages.append(msg1)
    expected_messages.append(msg2)

    assert len(messages) == len(expected_messages)
    for msg, expected_msg in zip(messages, expected_messages):
        assert msg.sender == expected_msg.sender
        assert msg.recipient == expected_msg.recipient
        assert msg.message == expected_msg.message
        assert msg.timestamp == expected_msg.timestamp

    mock_client.sendall.assert_called()


def test_retrieve_new_attribute_error(messenger, mock_socket):
    """Tests retrieve_new handles an AttributeError gracefully."""

    mock_client = MagicMock()
    mock_socket.return_value = mock_client

    mock_client.recv.return_value = json.dumps(
        {"response": {"invalid_key": "unexpected_value"}}
    ).encode()

    messenger.set_token("testtoken")

    messages = messenger.retrieve_new()

    assert messages is None


# pylint: disable=redefined-outer-name
def test_retrieve_all(messenger, mock_socket):
    """Tests retrieving all messages."""

    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_response = {
        "response": {
            "type": "ok",
            "messages": [
                {"from": "user1",
                 "message": "Hi!",
                 "timestamp": "2025-02-28T12:34:56"},
                {
                    "from": "user2",
                    "message": "Hello!",
                    "timestamp": "2025-02-28T12:35:00",
                },
            ],
        }
    }
    mock_client.recv.return_value = json.dumps(mock_response).encode()

    messenger.set_token("testtoken")
    messages = messenger.retrieve_all()

    expected_messages = []

    msg1 = DirectMessage()
    msg1.sender = "user1"
    msg1.recipient = "testuser"
    msg1.message = "Hi!"
    msg1.timestamp = "2025-02-28T12:34:56"

    msg2 = DirectMessage()
    msg2.sender = "user2"
    msg2.recipient = "testuser"
    msg2.message = "Hello!"
    msg2.timestamp = "2025-02-28T12:35:00"

    expected_messages.append(msg1)
    expected_messages.append(msg2)

    assert len(messages) == len(expected_messages)
    for msg, expected_msg in zip(messages, expected_messages):
        assert msg.sender == expected_msg.sender
        assert msg.recipient == expected_msg.recipient
        assert msg.message == expected_msg.message
        assert msg.timestamp == expected_msg.timestamp

    mock_client.sendall.assert_called()


# pylint: disable=redefined-outer-name
def test_retrieve_all_no_messages(messenger, mock_socket):
    """Tests retrieving all messages when there are none."""
    mock_client = MagicMock()
    mock_socket.return_value = mock_client
    mock_response = {"response": {"type": "ok", "messages": []}}
    mock_client.recv.return_value = json.dumps(mock_response).encode()

    messenger.set_token("testtoken")
    messages = messenger.retrieve_all()

    assert messages == []


@pytest.mark.usefixtures("messenger", "mock_socket_client")
# pylint: disable=redefined-outer-name
def test_client_socket(messenger, mock_socket_client):
    """Tests establishing a client socket connection."""

    mock_conn = MagicMock()
    mock_socket_client.return_value = mock_conn
    join_response = {
        "response": {
            "type": "ok",
            "message": "Welcome back!",
            "token": "testtoken"}
    }
    mock_conn.sendall = MagicMock()
    mock_conn.recv.return_value = json.dumps(join_response).encode()
    client = messenger.client_socket("127.0.0.1", 3001, "asdasd", "sdfsdf")
    assert client is not None
    mock_conn.sendall.assert_called()


@pytest.mark.usefixtures("messenger", "mock_socket_client")
# pylint: disable=redefined-outer-name
def test_client_socket_error(messenger, mock_socket_client):
    """Tests handling of client socket when the user has no token."""

    mock_conn = MagicMock()
    mock_socket_client.return_value = mock_conn
    join_response = {"response": {"type": "ok", "message": "Unknown error."}}

    mock_conn.sendall = MagicMock()
    mock_conn.recv.return_value = json.dumps(join_response).encode()

    client = messenger.client_socket("127.0.0.1", 3001, "lalala", "pass")
    assert client is None
    mock_conn.sendall.assert_called()


@pytest.mark.usefixtures("messenger", "mock_socket_client")
# pylint: disable=redefined-outer-name
def test_client_socket_error_2(messenger, mock_socket_client):
    """Tests handling of client socket when server response type is error."""

    mock_conn = MagicMock()
    mock_socket_client.return_value = mock_conn
    join_response = {"response": {
        "type": "error",
        "message": "Unknown error."}}

    mock_conn.sendall = MagicMock()
    mock_conn.recv.return_value = json.dumps(join_response).encode()

    client = messenger.client_socket("127.0.0.1", 3001, "testuser", "testpass")

    assert client is None


@pytest.mark.usefixtures("messenger")
# pylint: disable=redefined-outer-name
def test_client_socket_exception(messenger):
    """Tests handling of client socket when server info is incorrect."""
    t_messenger = messenger
    client = t_messenger.client_socket("1234", 3001, "testuser", "testpass")

    assert client is None
