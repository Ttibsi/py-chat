import socket
import threading

# TODO: dataclass/namedtuple
clients: list[socket.socket] = []
usernames: list[bytes] = []


def broadcast(msg: bytes) -> None:
    [c.send(msg) for c in clients]


def handle_client(client: socket.socket) -> None:
    # TODO: Handle `/` messages like IRC does (perhaps the client turns the msg
    # into a JSON string that's sent to the server, such as
    # {"cmd": "send_msg", txt: "foo"} to have diferent commands implemented
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except Exception as e:
            print(f"ERROR: {e}")
            index = clients.index(client)
            clients.remove(client)
            client.close()

            if index is not None:
                alias = usernames[index]
                broadcast(
                    f"{alias.decode('utf-8')} has left the chat".encode(
                        "utf-8"
                    )
                )
                usernames.remove(alias)

            break


def serve() -> None:
    # TODO: Create a logging-style output for all messages on the server side
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # This is localhost:6789
    s.bind((socket.gethostname(), 6789))
    s.listen(5)

    print("Server listening...")
    # TODO: Write current session to log file?
    while True:
        clientsock, address = s.accept()
        print(f"Connection from {str(address)} established.")

        usernames.append(clientsock.recv(1024))
        clients.append(clientsock)
        user = usernames[-1].decode("utf-8")
        print(f"User {user} has joined the chat!".encode("utf-8"))
        broadcast(f"{user} has connected...".encode("utf-8"))
        clientsock.send("You are now connected".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(clientsock,))
        thread.start()
