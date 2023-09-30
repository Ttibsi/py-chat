import logging
import signal
import socket
import threading
import types

clients: list[socket.socket] = []
usernames: list[bytes] = []


def setup_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )


def broadcast(msg: bytes) -> None:
    [c.send(msg) for c in clients]


# TODO: "left the chat" message not working
def handle_client(client: socket.socket) -> None:
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
            if msg:
                logging.info(msg)
        except Exception as e:
            print(f"ERROR: {e}")
            index = clients.index(client)
            clients.remove(client)
            client.close()

            if index is not None:
                alias = usernames[index]
                broadcast(
                    f"{alias.decode('utf-8')}: has left the chat".encode(
                        "utf-8"
                    )
                )
                usernames.remove(alias)

            break


# TODO: Handle `/` messages like IRC does (perhaps the client turns the msg
# into a JSON string that's sent to the server, such as
# {"cmd": "send_msg", txt: "foo"} to have diferent commands implemented
def serve() -> None:
    def signal_handler(signal: int, frame: types.FrameType | None) -> None:
        print("Recieved SIGINT... shutting down")
        logger.info("Recieved SIGINT... shutting down")

        try:
            s.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        s.close()
        raise InterruptedError

    setup_logging()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    signal.signal(signal.SIGINT, signal_handler)

    # This is localhost:6789
    s.bind((socket.gethostname(), 6789))
    s.listen(5)

    logger = logging.getLogger()

    print("Server listening...")
    logger.info("Server listening")

    while True:
        clientsock, address = s.accept()

        usernames.append(clientsock.recv(1024))
        clients.append(clientsock)
        user = usernames[-1].decode("utf-8")
        print(f"User {user} has joined the chat!".encode("utf-8"))
        broadcast(f"{user}: has connected...".encode("utf-8"))
        logger.info(f"{user}: has connected...")

        thread = threading.Thread(
            target=handle_client, args=(clientsock,), daemon=True
        )
        thread.start()
