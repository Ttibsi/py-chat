import os
import socket
import threading


def client_recv(s: socket.socket) -> None:
    while True:
        try:
            print(s.recv(1024).decode("utf-8"))
        except Exception as e:
            print(f"ERROR: {e}")
            s.close()
            break


def client_send(user: str, s: socket.socket) -> None:
    while True:
        msg = f"{user}: {input('')}"
        s.send(msg.encode("utf-8"))


def start() -> None:
    user = input("Enter username: ")
    if not user:
        # If no username specified, use computer name
        if os.name == "posix":
            user = os.environ["USER"]
        elif os.name == "nt":  # windows
            user = os.environ["USERDOMAIN"]
        else:
            print("OS not supported")
            return

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # TODO: Replace gethostname with a server ip -- perhaps entered by the
    # user at startup?
    s.connect((socket.gethostname(), 6789))
    s.send(user.encode("utf-8"))

    threading.Thread(target=client_recv, args=(s,)).start()
    threading.Thread(target=client_send, args=(user, s)).start()
