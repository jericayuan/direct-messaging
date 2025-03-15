# Name: Jerica Yuan
# Email: jxyuan@uci.edu
# ID: 73288143


from ds_protocol import (
    direct_message_request,
    send_message_request, 
    create_join_request,
    extract_json
)
from ds_messenger import DirectMessage, DirectMessenger
import socket

SERVER = "127.0.0.1"
PORT = 3001

def start_client(server, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server,port))

        # join_request = create_join_request("sally", "1234")
        # client.sendall(join_request.encode() + b"\r\n")
        # print("sally profile creation:")
        # print(extract_json(client.recv(4096).decode().strip()))

        join_request = create_join_request("jsmith", "1234")
        client.sendall(join_request.encode() + b"\r\n")
        response = client.recv(4096).decode().strip()
        parsed_response = extract_json(response)
        print("\njsmith profilie creation:")
        print(response)
        print(parsed_response)

        user_token = parsed_response.token

        msg_request = send_message_request(user_token, "sally", "Hi, Sally!", "")
        client.sendall(msg_request.encode() + b'\r\n')

        server_response = client.recv(4096).decode().strip()
        parsed_server_response = extract_json(server_response)
        print("\njsmith message dm send status:")
        print(parsed_server_response)

        # join_request = create_join_request("sally", "1234")
        # client.sendall(join_request.encode() + b"\r\n")
        # open_sally = extract_json(client.recv(4096).decode().strip())
        # print("\nopening sally profile:", open_sally)
        # sally_token = open_sally.token


        # ds_messenger = DirectMessenger("127.0.0.1", "sally", "1234")
        # dms_all = ds_messenger.retrieve_all()
        # print(dms_all)
        # ds = DirectMessenger()
        # dm_all = ds.retrieve_all()
        # client.sendall(dm_all.encode() + b'\r\n')
        # print("\nsally all messages:")
        # print(extract_json(client.recv(4096).decode().strip()))

        # print((client.recv(4096).decode().strip()))

        # dm_new = direct_message_request(sally_token, "all")
        # client.sendall(dm_new.encode() + b'\r\n')
        # print("\nsally new messages:")
        # print(extract_json(client.recv(4096).decode().strip()))

if __name__ == "__main__":
    start_client(SERVER, PORT)