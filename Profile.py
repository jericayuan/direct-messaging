# Profile.py
#
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
    pass



class DsuProfileError(Exception):
    pass


class Post(dict):
    """

    The Post class is responsible for working with individual user posts.
    It currently
    supports two features: A timestamp property that is set upon
    instantiation and
    when the entry object is set and an entry
    property that stores the post message.

    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        self._entry = entry
        dict.__setitem__(self, "entry", entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry

    def set_time(self, time: float):
        self._timestamp = time
        dict.__setitem__(self, "timestamp", time)

    def get_time(self):
        return self._timestamp

    """
    The property method is used to support get and set capability for entry and
    time values. When the value for entry is changed,
    or set, the timestamp field is
    updated to the current time.

    """
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ""
        self._message = []
        self.friends = []

    """

    add_post accepts a Post object as parameter and
    appends it to the posts list. Posts
    are stored in a list object in the order they are added.
    So if multiple Posts objects
    are created, but added to the Profile in a different order,
    it is possible for the
    list to not be sorted by the Post.timestamp property.
    So take caution as to how you
    implement your add_post code.

    """

    def add_message(self, message: Post) -> None:
        self._message.append(message)

    
    """
    get_posts returns the list object containing all posts
    that have been added to the
    Profile object

    """

    def get_posts(self) -> list[Post]:
        return self._message

   
    def add_friend(self, friend:str) -> None:
        if friend not in self.friends:
            self.friends.append(friend)
    
    def save_profile(self, path: str) -> None:
        p = Path(path)
        all_profiles = []
        profile_found = False

        if p.exists() and p.suffix == ".dsu":
            try:
                with open(p, "r") as f:
                    for line in f:
                        profile_data = json.loads(line.strip())
                        if profile_data["username"] == self.username:
                            profile_data = self.__dict__
                            profile_found = True
                        all_profiles.append(profile_data)
                
                with open(p, "w") as f:
                    for profile in all_profiles:
                        f.write(json.dumps(profile) + "\n")
                    if not profile_found:
                        f.write(json.dumps(self.__dict__) + "\n")
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            with open(p, "w") as f:
                f.write(json.dumps(self.__dict__) + "\n")

    def load_profile(self, path: str, username) -> None:
        p = Path(path)

        if p.exists() and p.suffix == ".dsu":
            try:
                with open(p, 'r') as f:
                    for line in f:
                        obj = json.loads(line.strip())
                        if obj['username'] == username:
                            self.password = obj["password"]
                            self.dsuserver = obj["dsuserver"]
                            self.bio = obj["bio"]
                            self.friends = obj.get("friends", [])
                            for message_obj in obj.get('message', []):
                                post = Post(message_obj["entry"], message_obj["timestamp"])
                                self._message.append(post)
                            return True
                    return False
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError('Profile not found.')
