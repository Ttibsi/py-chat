import os
import random
import socket
import threading

from textual import log
from textual import work
from textual.app import App
from textual.app import ComposeResult
from textual.containers import Container
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button
from textual.widgets import Header
from textual.widgets import Input
from textual.widgets import Label
from textual.widgets import Static


class Window(App):
    messages: reactive[tuple[str]] = reactive(())
    connected_users: list[str] = []
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        # if os.name == "posix":
        #     self.user = os.environ["USER"]
        # elif os.name == "nt":  # windows
        #     self.user = os.environ["USERDOMAIN"]
        # else:
        #     return

        self.user = str(random.randint(0, 10))
        self.title = "Py-Chat Client"

        # TODO: Replace gethostname with a server ip -- perhaps entered by the
        # user at startup?
        self.send_sock.connect((socket.gethostname(), 6789))
        self.send_sock.send(self.user.encode("utf-8"))
        self.client_recv()

    @work(exclusive=True, thread=True)
    def client_recv(self):
        log("STARTING SUB THREAD")
        while True:
            try:
                self.messages += self.recv_sock.recv(1024).decode("utf-8")
                log("TOTAL MESSAGES: " + self.messages)
            except Exception as e:
                print(f"ERROR: {e}")
                self.recv_sock.close()
                break

            view = self.query_one("#history", Static)
            view.update("\n".join(self.messages))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # only button currently is "submit"
        log("BUTTON PRESS")
        msg = self.query_one("#input").value
        self.query_one("#input").value = ""

        msg_to_send = f"{self.user}: {msg}"
        log("MSG_TO_SEND: " + msg_to_send)
        self.send_sock.send(msg_to_send.encode("utf-8"))
