# Name: Jerica Yuan
# Email: jxyuan@uci.edu
# ID: 73288143


from ds_protocol import extract_json, send_message_request, direct_message_request, create_join_request
import socket
import json
from collections import namedtuple

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None
    self.sender = None
  
  def get_message_details(self):
     MessageData = namedtuple("MessageData", ["sender", "recipient", "message", "timestamp"])
     message_details = MessageData(self.sender, self.recipient, self.message, self.timestamp)
     return message_details
   


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver
    self.username = username
    self.password = password

  def retrieve_token(self):
        return self.token
  
  def set_token(self, token):
        self.token = token

  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    client = self.client_socket(self.dsuserver, 3001, self.username, self.password)
    request = send_message_request(self.retrieve_token(), recipient, message, "")
    client.sendall(request.encode() + b'\r\n')
    response = extract_json(client.recv(4096).decode().strip())

    if response.type == "ok":
       return True
    else:
       return False

  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new 
    client = self.client_socket(self.dsuserver, 3001, self.username, self.password)
    request = direct_message_request(self.retrieve_token(), "new")
    client.sendall(request.encode() + b'\r\n')
    response = extract_json(client.recv(4096).decode().strip())
    new_messages = []
    if response.message:
       for message in response.message:
          message_details = DirectMessage()
          message_details.sender = message["from"]
          message_details.recipient = self.username
          message_details.message = message["message"]
          message_details.timestamp = message["timestamp"]
          new_messages.append(message_details.get_message_details())
    return new_messages
          
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    client = self.client_socket(self.dsuserver, 3001, self.username, self.password)
    request = direct_message_request(self.retrieve_token(), "all")
    client.sendall(request.encode() + b'\r\n')
    response = extract_json(client.recv(4096).decode().strip())
    all_messages = []
    if response.message:
       for message in response.message:
          message_details = DirectMessage()
          message_details.sender = message["from"]
          message_details.recipient = self.username
          message_details.message = message["message"]
          message_details.timestamp = message["timestamp"]
          all_messages.append(message_details.get_message_details())
    return all_messages

  
  def client_socket(self, server: str, port: str, username: str, password: str):
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

          print("Returning client...")
          return client
      except (socket.error, json.JSONDecodeError) as e:
        print("Failed to connect to server.")
        client.close()
        return None
            