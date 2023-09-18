import os
import socket
import threading

from textual.app import App
from textual.app import ComposeResult
from textual.containers import Container
from textual.containers import VerticalScroll
from textual.widgets import Button
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Static


def client_recv(s: socket.socket, m: list[str]) -> None:
    while True:
        try:
            m.append(s.recv(1024).decode("utf-8"))
        except Exception as e:
            print(f"ERROR: {e}")
            s.close()
            break


class Window(App):
    messages: list[str] = []
    connected_users: list[str] = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user = ""

    def compose(self) -> ComposeResult:
        yield Header()

        with Container():
            # TODO: Fill out this label (or as a Static) for all connected
            # users - could detect a "user has joined/left the chat" message
            yield Label("Users")
            with VerticalScroll():
                yield Static("Messages", id="history")

        with Container():
            yield Input(id="input")
            yield Button("Submit", id="submit")

    def on_mount(self) -> None:
        # Connect to sockets here
        # TODO: Username input
        if os.name == "posix":
            self.user = os.environ["USER"]
        elif os.name == "nt":  # windows
            self.user = os.environ["USERDOMAIN"]
        else:
            return

        # TODO: Replace gethostname with a server ip -- perhaps entered by the
        # user at startup?
        self.sock.connect((socket.gethostname(), 6789))
        self.sock.send(self.user.encode("utf-8"))

        recv_thread = threading.Thread(
            target=client_recv, args=(self.sock, self.messages)
        )
        recv_thread.start()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # only button currently is "submit"
        msg = self.query_one("#input").value
        self.messages.append(msg)  # TODO: Remove this
        self.query_one("#input").value = ""

        # This updates our view for our messages - need to add view update for
        # recieved messages too
        view = self.query_one("#history", Static)
        view.update("\n".join([i for i in self.messages]))

        msg_to_send = f"{self.user}: {msg}"
        self.sock.send(msg_to_send.encode("utf-8"))
