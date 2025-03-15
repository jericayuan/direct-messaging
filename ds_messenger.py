# Name: Jerica Yuan
# Email: jxyuan@uci.edu
# ID: 73288143
"""
Direct Messaging Module

This module provides classes and methods to facilitate direct messaging
via a server connection. It includes functionality to send and retrieve
messages, as well as handle authentication.

Classes:
    DirectMessage: Represents a single direct message.
    DirectMessenger: Manages sending, retrieving,
    and authentication for messages.

Functions:
    extract_json: Extracts JSON from a response string.
    send_message_request: Creates a request to send a message.
    direct_message_request: Creates a request to retrieve messages.
    create_join_request: Creates a request to join the server.
"""
import socket
import json
from ds_protocol import (
    extract_json,
    send_message_request,
    direct_message_request,
    create_join_request,
)


class DirectMessage:
    """Represents a direct message sent between users."""

    def __init__(self):
        """Initializes an empty DirectMessage instance."""

        self.recipient = None
        self.message = None
        self.timestamp = None
        self.sender = None

    def __str__(self):
        """Returns a formatted string representation of the direct message."""

        return (f"[{self.timestamp}] {self.sender} "
                f"-> {self.recipient}: {self.message}")

    def __repr__(self):
        """Returns a developer-friendly string
        representation of the direct message."""

        return (f"DirectMessage(sender='{self.sender}', "
                f"recipient='{self.recipient}', message='{self.message}', "
                f"timestamp='{self.timestamp}')")


class DirectMessenger:
    """Handles direct messaging operations such as
    sending and retrieving messages."""

    def __init__(self, dsuserver=None, username=None, password=None):
        """
        Initializes DirectMessenger with server, username, and password.
        Args:
            dsuserver (str, optional): The messaging server address.
            username (str, optional): The username for authentication.
            password (str, optional): The password for authentication.
        """

        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def retrieve_token(self):
        """Retrieves the stored authentication token.

        Returns:
                str: The authentication token.
        """
        return self.token

    def set_token(self, token):
        """Sets the authentication token.

        Args:
                token (str): The authentication token.
        """
        self.token = token

    def send(self, message: str, recipient: str) -> bool:
        """Sends a direct message to a recipient.

        Args:
                message (str): The message content.
                recipient (str): The recipient username.

        Returns:
                bool: True if message is successfully sent, False otherwise.
        """
        client = self.client_socket(self.dsuserver, 3001,
                                    self.username, self.password)
        request = send_message_request(self.retrieve_token(),
                                       recipient, message, "")
        client.sendall(request.encode() + b"\r\n")
        response = extract_json(client.recv(4096).decode().strip())

        if response.type == "ok":
            return True
        return False

    # pylint: disable=inconsistent-return-statements
    def retrieve_new(self) -> list:
        """Retrieves new messages from the server.

        Returns:
            list: A list of DirectMessage objects containing new messages.
        """
        client = self.client_socket(self.dsuserver, 3001,
                                    self.username, self.password)
        request = direct_message_request(self.retrieve_token(), "new")
        try:
            client.sendall(request.encode() + b"\r\n")
            response = extract_json(client.recv(4096).decode().strip())
            new_messages = []
            if response.message:
                for message in response.message:
                    message_details = DirectMessage()

                    message_details.sender = message.get("from", self.username)
                    message_details.recipient = message.get("recipient",
                                                            self.username)

                    message_details.message = message.get("message")
                    message_details.timestamp = message.get("timestamp")
                    new_messages.append(message_details)
            return new_messages
        except AttributeError:
            pass

    def retrieve_all(self) -> list:
        """Retrieves all messages from the server.

        Returns:
                list: A list of DirectMessage objects containing all messages.
        """
        # must return a list of DirectMessage objects containing all messages
        client = self.client_socket(self.dsuserver, 3001,
                                    self.username, self.password)
        request = direct_message_request(self.retrieve_token(), "all")
        client.sendall(request.encode() + b"\r\n")
        response = extract_json(client.recv(4096).decode().strip())
        all_messages = []
        if response.message:
            for message in response.message:
                message_details = DirectMessage()

                message_details.sender = message.get("from", self.username)
                message_details.recipient = message.get("recipient",
                                                        self.username)
                message_details.message = message.get("message")
                message_details.timestamp = message.get("timestamp")
                all_messages.append(message_details)
        return all_messages

    def client_socket(self, server: str, port: str,
                      username: str, password: str):
        """Creates and returns a socket connection to the server.

        Args:
                server (str): The server address.
                port (int): The server port.
                username (str): The username for authentication.
                password (str): The password for authentication.

        Returns:
                socket.socket: A connected socket object or None on failure.
        """
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server, port))

            join_request = create_join_request(username, password)
            client.sendall(join_request.encode() + b"\r\n")

            response = client.recv(4096).decode().strip()
            parsed_response = extract_json(response)

            if parsed_response.type == "error":
                print("[ERROR]", parsed_response.message)
                client.close()
                return None

            if not parsed_response.token:
                print("[ERROR] No token received. Authentication failed.")
                client.close()
                return None

            self.set_token(parsed_response.token)

            return client
        except (socket.error, json.JSONDecodeError) as e:
            print("Failed to connect to server.", e)
            client.close()
            return None
