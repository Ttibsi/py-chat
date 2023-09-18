# import os
# import socket
# import threading
#
# from textual.app import App
# from textual.app import ComposeResult
# from textual.containers import ScrollableContainer
# from textual.widgets import Header
# from textual.widgets import Input
# from textual.widgets import Label
# from textual.widgets import Static
#
# def client_recv(s: socket.socket, m: list[str]) -> None:
#     global msgs
#     while True:
#         try:
#             m.text.append(s.recv(1024).decode("utf-8"))
#         except Exception as e:
#             print(f"ERROR: {e}")
#             s.close()
#             break
#
#
# def client_send(user: str, s: socket.socket) -> None:
#     while True:
#         msg = f"{user}: {input('')}"
#         s.send(msg.encode("utf-8"))
#
#
# class Message(Static):
#     def on_mount(self) -> None:
#         for msg in msgs.text:  # NOTE: This can't see `m` yet
#             yield Label(msg)
#         while True:
#             self.refresh()
#
#
# class Entry(Static):
#     # https://textual.textualize.io/widget_gallery/#input
#     def compose(self) -> ComposeResult:
#         yield Input(placeholder="Enter message:")
#         # TODO: Figure out how to get the text to the "client_send" thread
#
#
# class Window(App):
#     def compose(self) -> ComposeResult:
#         # Create child widgets
#         yield Header()
#         yield ScrollableContainer(Message())
#         yield Entry()
#
#     def on_mount(self) -> None:
#         # When we start up
#
#         # TODO: Move this to the entry window on startup
#         user = input("Enter username: ")
#         if not user:
#             # If no username specified, use computer name
#             if os.name == "posix":
#                 user = os.environ["USER"]
#             elif os.name == "nt":  # windows
#                 user = os.environ["USERDOMAIN"]
#             else:
#                 print("OS not supported")
#                 return
#
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# TODO: Replace gethostname with a server ip -- perhaps entered by the
#         # user at startup?
#         s.connect((socket.gethostname(), 6789))
#         s.send(user.encode("utf-8"))
#
#         msgs: list[str] = []
#         threading.Thread(target=client_recv, args=(s, msgs)).start()
#         threading.Thread(target=client_send, args=(user, s)).start()
