"""
Profile management module for handling user data, messages, and authentication.

This module provides functionality for:
- Managing user profiles (saving, loading)
- Handling messages (sent, received)
- Managing friends list
- Password authentication

It supports JSON serialization for persistent storage.
"""

# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND
# THE JSON SERIALIZATION ASPECTS OF THIS CODE
# RIGHT NOW, though can you certainly take a look at it
# if you are curious since we
# already covered a bit of the JSON format in class.
#


import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """Exception raised for errors related to DSU file operations."""
    print("ERROR related to DSU file operations.")


class DsuProfileError(Exception):
    """Exception raised for errors related to loading or
    processing user profiles."""
    print("ERROR related to DSU profile operations.")


class Post(dict):
    """Represents a user post, including its content and timestamp."""

    def __init__(self, entry: str = None, timestamp: float = 0):
        """
        Initializes a Post object.

        Args:
            entry (str, optional): The text content of the post.
            Defaults to None.
            timestamp (float, optional): The timestamp of the post.
            Defaults to 0.
        """
        self._timestamp = timestamp
        self.set_entry(entry)

        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """
        Sets the content of the post.

        Args:
            entry (str): The post content.
        """
        self._entry = entry
        dict.__setitem__(self, "entry", entry)

        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        """Returns the content of the post."""

        return self._entry

    def set_time(self, time: float):  # pylint: disable=redefined-outer-name
        """Sets the timestamp of the post."""

        self._timestamp = time
        dict.__setitem__(self, "timestamp", time)

    def get_time(self):
        """Returns timestamp of post"""
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """Represents a user profile with messages,
    friends, and authentication details."""

    def __init__(self, dsuserver=None, username=None, password=None):
        """
        Initializes a Profile object.

        Args:
            dsuserver (str, optional): The DSU server address.
            Defaults to None.
            username (str, optional): The username of the profile.
            Defaults to None.
            password (str, optional): The user's password. Defaults to None.
        """
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ""
        self.message_sent = []
        self.message_received = []
        self.friends = []

    def add_message_sent(self, recipient, timestamp, message: Post) -> None:
        """
        Adds a message to the list of sent messages.

        Args:
            recipient (str): The recipient's username.
            timestamp (float): The time when the message was sent.
            message (Post): The message object.
        """
        self.message_sent.append(
            {"to": recipient, "message": message, "timestamp": timestamp}
        )

    def add_message_received(self, sender, timestamp, message: Post) -> None:
        """
        Adds a message to the list of received messages.

        Args:
            sender (str): The sender's username.
            timestamp (float): The time when the message was received.
            message (Post): The message object.
        """
        self.message_received.append(
            {"from": sender, "message": message, "timestamp": timestamp}
        )

    def get_message_sent(self) -> list[Post]:
        """Returns a list of messages sent."""

        return self.message_sent

    def add_friend(self, friend: str) -> None:
        """
        Adds a friend to the user's friend list.

        Args:
            friend (str): The friend's username.
        """
        if friend not in self.friends:
            self.friends.append(friend)

    def get_friends(self):
        """Returns the list of friends."""

        return self.friends

    def check_user_password(self, username, password, path):
        """
        Checks if the given username and password match the stored credentials.

        Args:
            username (str): The username to check.
            password (str): The password to verify.
            path (Path): The path to the user profile file.

        Returns:
            bool: True if credentials are correct, False otherwise.
        """
        p = path
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = f.read().strip()
                    if not data:
                        return False
                    profile_data = json.loads(data)
                    if profile_data["username"] == username:
                        if password == profile_data["password"]:
                            return True
                        return False
            except Exception as e:
                raise DsuFileError("Error in collecting data", e) from e
        return False

    def save_profile(self, username, password, path: str) -> bool:
        """
        Saves the user's profile data to a .dsu file.

        Args:
            username (str): The username of the profile.
            password (str): The user's password.
            path (str): The file path to save the profile.

        Returns:
            bool: True if the profile is successfully saved, False otherwise.
        """
        p = Path(path)

        profile_dict = self.__dict__.copy()
        for key, value in profile_dict.items():
            if isinstance(value, Path):
                profile_dict[key] = str(value)

        profile_dict["friends"] = self.friends
        profile_dict["message_sent"] = self.message_sent
        profile_dict["message_received"] = self.message_received

        try:
            if p.exists() and p.suffix == ".dsu":
                with open(p, "r+", encoding="utf-8") as f:
                    f.seek(0)
                    existing_data = f.read().strip()

                    if existing_data:
                        try:
                            content = json.loads(existing_data)
                        except json.JSONDecodeError:
                            print(
                                f"ERROR: Corrupted JSON in {p}."
                            )
                            content = {}
                            return False
                        if content.get("username") != username:
                            return False
                        if not self.check_user_password(username, password, p):
                            return False

                        content.update(profile_dict)
                        profile_dict = content

                    f.seek(0)
                    f.truncate()
                    json.dump(profile_dict, f, indent=4)

                print(f"DEBUG: Saved for {username} at {p}")
                return True
            with open(p, "w", encoding="utf-8") as f:
                json.dump(profile_dict, f, indent=4)
            print(f"DEBUG: New profile created for {username} at {p}")
            return True

        except Exception as ex:
            print(f"ERROR: Failed to save profile for {username}: {ex}")
            raise DsuFileError("Error in processing DSU file.", ex) from ex

    def load_profile(self, username, path: str):
        """
        Loads a user profile from a .dsu file.

        Args:
            username (str): The username of the profile.
            path (str): The file path to load the profile from.

        Returns:
            bool: True if the profile was successfully loaded, False otherwise.
        """
        p = Path(path)
        if not p.exists():
            return False
        if p.suffix == ".dsu":
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = f.read().strip()
                    if not data:
                        return False

                    obj = json.loads(data)
                    if obj["username"] != username:
                        return False

                    if obj["username"] == username and \
                        self.check_user_password(
                        self.username, self.password, p
                    ):
                        self.password = obj["password"]
                        self.dsuserver = obj["dsuserver"]
                        self.bio = obj["bio"]
                        self.friends = obj.get("friends", [])
                        self.message_sent = obj.get("message_sent", [])
                        self.message_received = obj.get("message_received", [])
                        return True
                    return False
            except Exception as ex:
                raise DsuProfileError(ex) from ex
        return False
