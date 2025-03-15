ICS 32 Distributed Social Messenger: a4

Name: Jerica Yuan
Email: jxyuan@uci.edu
StudentId: 73288143


---

ProjectOverview:
This project is a Distributed Social Messenger that lets users send and receive direct messages
from other user profiles, manage user profiles, and interact with a server-based messaging system. 

---

Features:
- A Graphical User Interface (GUI) for messaging.
- User authentication and profile management.
- Direct messaging features (send, receive, and retrieve messages).
- Server interaction for storing and managing messages.

---

File Descriptions:
a4.py
- Main entry point for the GUI-based messaging application.

ds_protocol.py
- Defines the Direct Social Protocol (DSP) for sending and receiving messages.

ds_messenger.py	
- Implements the DirectMessenger class to send and retrieve messages.

ics32_profile.py
- Handles user profiles, authentication, and data storage.

server.py
- A TCP server that manages messaging, authentication, and data storage.


Test Files:
test_ds_message_protocol.py
- Unit tests for ds_protocol.py.
test_ds_messenger.py
- Unit tests for ds_messenger.py.

---

Tests Ran:

- utilized pytest and coverage
- python -m coverage run -m pytest .
- python -m coverage run -m --branch pytest . 
- python -m coverage report -m

---

Usage:
 1. Start DSU server
    - python server.py
 2. Start chat application
    - python a4.py
 3. Open 'Settings' dropdown, and configure the server to create a profile or sign interact
 4. Enter all required fields of configure server.
 5. Add contacts to start chatting.
