'''
a4.py contains if __name__ == "__main__", and is the entry into the program.
Main application module for managing user profiles and messaging.

This module handles GUI interaction, server configuration, user authentication,
and real-time messaging updates.
'''
# NAME - Jerica Yuan
# EMAIL - jxyuan@uci.edu
# STUDENT ID - 73288143

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sys
from pathlib import Path
from datetime import datetime
import ics32_profile
from ds_messenger import DirectMessenger


class Body(ttk.Frame):
    """The main body of the application,
    handling UI components for messages and contacts."""

    def __init__(self, root, recipient_selected_callback=None):
        """Initialize the chat body with UI elements."""

        ttk.Frame.__init__(self, root)
        self.root = root
        self.contacts = []
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, _event):
        """Handles contact selection from the UI."""

        try:
            index = int(self.posts_tree.selection()[0])
            entry = self.contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)
        except IndexError:
            pass

    def insert_contact(self, contact: str):
        """Inserts a contact into the contact list."""

        self.contacts.append(contact)
        num = len(self.contacts) - 1
        self._insert_contact_tree(num, contact)

    def _insert_contact_tree(self, num, contact: str):
        """Helper method to insert a contact into the TreeView UI."""

        if len(contact) > 25:
            contact = contact[:24] + "..."
        num = self.posts_tree.insert("", num, num, text=contact)

    def insert_user_message(self, message: str):
        """Displays a user-sent message in the chat UI."""

        max_width = 30
        wrapped_message = "\n".join(
            message[i:i + max_width] for i in range(0, len(message), max_width)
        )
        self.entry_editor.insert(tk.END, wrapped_message + "\n", "entry-right")
        self.entry_editor.see(tk.END)

    def insert_contact_message(self, message: str):
        """Displays a received message from a contact in the chat UI."""

        max_width = 30
        wrapped_message = "\n".join(
            message[i:i + max_width] for i in range(0, len(message), max_width)
        )
        self.entry_editor.insert(tk.END, wrapped_message + "\n", "entry-left")
        self.entry_editor.see(tk.END)

    def get_text_entry(self) -> str:
        """Retrieves the current text entered
        by the user in the chat input box."""

        return self.message_editor.get("1.0", "end").rstrip()

    def set_text_entry(self, text: str):
        """Sets the text in the message entry field."""

        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """Initializes and lays out all UI components in the chat body."""

        style = ttk.Style()
        style.configure("TFrame", background="#F3F3F3")
        style.configure("Modern.TEntry", padding=15,
                        borderwidth=2, relief="flat")

        posts_frame = ttk.Frame(master=self, width=250, style="Frame.TFrame")
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>",
                             self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = ttk.Frame(master=self, style="Frame.TFrame")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.chat_header = ttk.Frame(entry_frame, style="Frame.TFrame")
        self.chat_header.pack(fill=tk.X, side=tk.TOP)

        self.recipient_label = ttk.Label(
            self.chat_header,
            text="",
            font=("Arial", 14, "bold"),
            anchor="center",
            justify="center",
        )
        self.recipient_label.pack(fill=tk.X, pady=5)

        editor_frame = ttk.Frame(master=entry_frame, style="Frame.TFrame")
        editor_frame.pack(fill=tk.BOTH,
                          side=tk.LEFT, expand=True)

        scroll_frame = ttk.Frame(master=entry_frame,
                                 width=10, style="Frame.TFrame")
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = ttk.Frame(master=self, style="Frame.TFrame")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(self, height=3, width=50, wrap="word")
        self.message_editor.pack(
            fill=tk.BOTH, side=tk.LEFT,
            expand=True, padx=5, pady=5
        )
        self.entry_editor = tk.Text(editor_frame,
                                    width=40, height=5, wrap="word")
        self.entry_editor.tag_configure("entry-right", justify="right")
        self.entry_editor.tag_configure("entry-left", justify="left")
        self.entry_editor.pack(fill=tk.BOTH,
                               side=tk.LEFT, expand=True,
                               padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(
            master=scroll_frame, command=self.entry_editor.yview
        )
        self.entry_editor["yscrollcommand"] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(
            fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0
        )


# pylint: disable=too-many-ancestors
class Footer(ttk.Frame):
    """Footer section of the chat containing the send button."""

    def __init__(self, root, send_callback=None):
        """Initialize the footer with a send button."""

        ttk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """Handles the event when the send button is clicked."""

        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """Draws the footer UI including the send button."""

        style = ttk.Style()
        style.configure(
            "ModernTButton",
            font=("Arial", 8, "bold"),
            foreground="white",
            background="#0078D7",
            borderwidth=2,
        )
        style.map(
            "Modern.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[("pressed", "#005A9E"), ("active", "#005A9E")],
        )

        save_button = ttk.Button(
            master=self,
            text="Send",
            width=8,
            command=self.send_click,
            style="Modern.TButton",
        )
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = ttk.Label(master=self, text="No Account Active.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


# pylint: disable=too-many-instance-attributes
class NewContactDialog(tk.simpledialog.Dialog):
    """Dialog window for adding a new contact or configuring an account."""

    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        root,
        title=None,
        user=None,
        pwd=None,
        server=None,
        file_path=None,
        file_name=None,
    ):
        """Initialize the dialog with user details for configuring a server."""

        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        self.file_path = file_path
        self.file_name = file_name
        self.canceled = True
        super().__init__(root,
                         title)

    def body(self, master):
        """Creates the form layout for entering account details."""

        self.server_label = ttk.Label(master,
                                      width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = ttk.Entry(master, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack(padx=20)

        self.username_label = ttk.Label(master, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = ttk.Entry(master, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack(padx=20)

        self.password_label = ttk.Label(master, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = ttk.Entry(master, width=30)
        self.password_entry["show"] = "*"
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack(padx=20)

        self.file_path_label = ttk.Label(master,
                                         width=30, text="File Path (Folder)")
        self.file_path_label.pack()
        self.file_path_entry = ttk.Entry(master, width=30)
        self.file_path_entry.insert(tk.END, self.file_path)
        self.file_path_entry.pack(padx=20)

        self.file_name_label = ttk.Label(master, width=30, text="File Name")
        self.file_name_label.pack()
        self.file_name_entry = ttk.Entry(master, width=30)
        self.file_name_entry.insert(tk.END, self.file_name)
        self.file_name_entry.pack(padx=20)
        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        # self.password...

        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.server_entry.delete(0, tk.END)
        self.file_path_entry.delete(0, tk.END)
        self.file_name_entry.delete(0, tk.END)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        return master

    def buttonbox(self):
        """Customize default OK and Cancel buttons."""
        box = ttk.Frame(self)

        self.ok_button = ttk.Button(box, text="OK", command=self.ok, width=7)
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.cancel_button = ttk.Button(
            box, text="Cancel", command=self.cancel, width=7
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

        box.pack()
        self.bind("<Return>", self.on_enter_key)

    def on_enter_key(self, _event):
        """Handles the enter key event to submit the form."""

        self.ok()

    def apply(self):
        """Retrieves entered data when the dialog is confirmed."""

        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()
        self.file_path = self.file_path_entry.get()
        self.file_name = self.file_name_entry.get()

        self.canceled = False
        self.destroy()

    def on_cancel(self):
        '''Closes program'''
        self.canceled = True
        self.destroy()


# pylint: disable=too-many-instance-attributes
class MainApp(ttk.Frame):
    """Main application class for managing the GUI and
    communication with the server."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, root):
        """Initialize the main application window.

        Args:
            root (tk.Tk): The root Tkinter window.
        """

        ttk.Frame.__init__(self, root)
        self.root = root
        self.username = ""
        self.password = ""
        self.server = ""
        self.recipient = ""
        self.ds_messenger = None
        self.file_path = ""
        self.file_name = ""
        self.user_file = ""
        self.profile = ""
        self.job = None

        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        # self.direct_messenger = ... continue!
        style = ttk.Style()
        style.theme_use("clam")

        bg_color = "#F3F3F3"
        text_color = "#333333"

        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=text_color)
        style.configure(
            "Modern.TButton",
            font=("Arial", 8, "bold"),
            foreground="white",
            borderwidth=2,
        )
        style.map(
            "Modern.TButton",
            foreground=[("pressed", "white"), ("active", "white")],
            background=[("pressed", "#004080"), ("active", "#005A9E")],
        )

        style.configure(
            "Modern.TEntry",
            padding=10,
            borderwidth=2,
            relief="flat",
            font=("Arial", 12),
        )

        style.configure("TFrame", background=bg_color)
        style.configure(
            "TLabelFrame", background=bg_color, foreground=text_color
        )
        self._draw()

    def set_profile(self):
        """Sets the user profile based on current
        username, password, and server.

        Returns:
            Profile: The configured Profile instance.
        """
        self.profile = ics32_profile.Profile(self.server,
                                             self.username, self.password)
        return self.profile

    def clear_profile(self):
        """Clears the current profile.

        Returns:
            Profile: A blank Profile instance.
        """
        self.profile = ics32_profile.Profile("", "", "")
        return self.profile

    def send_message(self):
        """Sends a message to the selected recipient.

        The message is saved locally and sent to the server.
        """
        # You must implement this!
        if not self.ds_messenger or not self.recipient:
            messagebox.showinfo("Error",
                                "Message could not be sent.")
            return

        message = self.body.get_text_entry()
        if message.strip():
            timestamp = datetime.now().timestamp()
            self.profile.add_message_sent(
                message=message, recipient=self.recipient,
                timestamp=timestamp
            )
            self.profile.save_profile(self.username,
                                      self.password, self.user_file)
            success = self.ds_messenger.send(message, self.recipient)
            if success:
                self.body.insert_user_message(message)
                self.body.set_text_entry("")
            else:
                messagebox.showerror("ERROR", "Message could not be sent!")

    def add_contact(self):
        """Adds a new contact to the user's friends list."""

        contact = simpledialog.askstring("Add Contact",
                                         "Enter contact username:")
        if self.profile:
            if not contact:
                return
            if contact in self.profile.get_friends():
                messagebox.showinfo("", "This person is already your friend!")
            elif contact == self.username:
                messagebox.showinfo("", "You can't add yourself!")
            else:
                self.body.insert_contact(contact)
                self.profile.add_friend(contact)
                self.profile.save_profile(self.username,
                                          self.password, self.user_file)
        else:
            messagebox.showerror("ERROR", "Please log in to add contacts!")
        self.body.set_text_entry("")

    def recipient_selected(self, recipient):
        """Handles selecting a recipient from the contacts list.

        Args:
            recipient (str): The selected recipient's username.
        """
        self.recipient = recipient
        self.body.entry_editor.delete("1.0", tk.END)

        self.body.recipient_label.config(text=self.recipient)
        self.body.chat_header.pack(fill=tk.X, side=tk.TOP)
        all_messages = []
        if self.profile and not self.ds_messenger:
            for message in self.profile.message_sent:
                all_messages.append(message)
            for message in self.profile.message_received:
                all_messages.append(message)
            sorted_messages = sorted(all_messages,
                                     key=lambda x: float(x["timestamp"]))
            for message in sorted_messages:
                if message.get("to") == self.recipient:
                    self.body.insert_user_message(message["message"])
                elif message.get("from") == self.recipient:
                    self.body.insert_contact_message(message["message"])

        if self.ds_messenger and self.ds_messenger.retrieve_token():
            all_messages = self.ds_messenger.retrieve_all()
            for message in all_messages:
                if (
                    message.recipient == self.recipient
                    and message.sender == self.username
                ):
                    self.body.insert_user_message(message.message)
                    self.body.set_text_entry("")
                elif (
                    message.recipient == self.username
                    and message.sender == self.recipient
                ):
                    self.body.insert_contact_message(message.message)

        self.body.entry_editor.update_idletasks()

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    def configure_server(self):
        """Handles user login and switching accounts,
        including server validation."""

        previous_username = self.username
        previous_password = self.password
        previous_server = self.server
        previous_file_path = self.file_path
        previous_file_name = self.file_name
        previous_user_file = self.user_file
        previous_profile = self.profile

        if self.job:
            self.root.after_cancel(self.job)

        ud = NewContactDialog(
            self.root,
            "Configure Account",
            self.username,
            self.password,
            self.server,
            (self.file_path),
            (self.file_name),
        )
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.file_path = Path(ud.file_path)
        self.file_name = ud.file_name + ".dsu"
        if ud.canceled:
            return

        temp_profile = ics32_profile.Profile(self.server,
                                             self.username, self.password)

        # self.set_profile()
        if self.username and self.password \
                and self.file_path and self.file_name:
            self.ds_messenger = ""

            self.file_path.mkdir(parents=True, exist_ok=True)

            temp_user_file = self.file_path / self.file_name

            if temp_user_file.exists():
                if not temp_profile.load_profile(self.username,
                                                 temp_user_file):
                    messagebox.showerror("ERROR",
                                         "Incorrect username or password!")
                    return

            self.body.entry_editor.delete("1.0", tk.END)

            if (
                not temp_profile.load_profile(self.username, temp_user_file)
                and self.server
            ):
                if not temp_profile.save_profile(
                    self.username, self.password, temp_user_file
                ):
                    messagebox.showerror("ERROR", "Could not retrieve info.")
                    return
            elif (
                not temp_profile.check_user_password(
                    self.username, self.password, temp_user_file
                )
                and self.username
            ):
                messagebox.showerror("ERROR", "Could not log in.")
                return

            if self.username and self.password and self.server:
                if not self.ds_messenger:
                    self.ds_messenger = DirectMessenger()
                    self.ds_messenger.dsuserver = self.server
                    self.ds_messenger.username = self.username
                    self.ds_messenger.password = self.password
                if (
                    self.ds_messenger.client_socket(
                        self.server, 3001, self.username, self.password
                    )
                    is None
                ):
                    messagebox.showerror("ERROR", "Invalid server location.")
                    self.username = previous_username
                    self.password = previous_password
                    self.server = previous_server
                    self.file_path = previous_file_path
                    self.file_name = previous_file_name
                    self.user_file = previous_user_file
                    self.profile = previous_profile
                    self.ds_messenger = None
                    self.ds_messenger = DirectMessenger()
                    self.ds_messenger.dsuserver = self.server
                    self.ds_messenger.username = self.username
                    self.ds_messenger.password = self.password
                    # self.server = ''

                self.job = self.root.after(2000, self.check_new)
            self.profile = temp_profile
            self.user_file = temp_user_file

            if self.profile.load_profile(self.username, self.user_file):
                self.body.posts_tree.unbind("<<TreeviewSelect>>")
                self.body.contacts.clear()
                for item in self.body.posts_tree.get_children():
                    self.body.posts_tree.delete(item)
                for friend in self.profile.friends:
                    self.body.insert_contact(friend)
                self.footer.footer_label.config(
                    text=f"Welcome, {self.username}!")
                self.footer.footer_label.pack()

            self.body.posts_tree.bind("<<TreeviewSelect>>",
                                      self.body.node_select)
        else:
            messagebox.showerror("ERROR", "Could not log in.")

        self.recipient = ""

        self.body.posts_tree.update_idletasks()

    def check_new(self):
        """Checks for new messages from the
        server and updates the chat window."""

        # You must implement this!
        if not self.server.strip() or not self.ds_messenger:
            return

        new_messages = self.ds_messenger.retrieve_new()
        if new_messages:
            for message in new_messages:
                sender = message.sender
                text = message.message
                timestamp = message.timestamp
                self.profile.add_message_received(
                    message=text, sender=sender, timestamp=timestamp
                )
                self.profile.save_profile(self.username,
                                          self.password, self.user_file)

                if sender == self.recipient:
                    self.body.insert_contact_message(text)

        self.job = self.root.after(2000, self.check_new)

    def close(self):
        """Closes the application."""

        self.root.quit()
        self.root.destroy()
        sys.exit()

    def _draw(self):
        """Creates the menu and initializes UI components."""

        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root["menu"] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label="File")
        menu_file.add_command(label="Close", command=self.close)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label="Settings")
        settings_file.add_command(label="Add Contact",
                                  command=self.add_contact)
        settings_file.add_command(
            label="Configure DS Server", command=self.configure_server
        )

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(
            fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add("*tearOff", False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    x_id = main.after(2000, app.check_new)
    print(x_id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
