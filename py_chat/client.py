import curses
import random
import socket
import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any

history: list[str] = []


def client_recv(s: socket.socket) -> None:
    while True:
        try:
            global history
            history.append(s.recv(1024).decode("utf-8"))
        except Exception as e:
            print(f"ERROR: {e}")
            s.close()
            break


def start_sockets(user: str) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # TODO: Replace gethostname with a server ip -- perhaps entered by the
    # user at startup?
    s.connect((socket.gethostname(), 6789))
    s.send(user.encode("utf-8"))

    threading.Thread(target=client_recv, args=(s,), daemon=True).start()

    return s


# TODO: Display list of connected users to the left
def c_main(stdscr: Window, default_colors: bool = False) -> int:
    global history
    # TODO: Custom username? At least read the user's machine name 
    user = f"User {random.randint(0,9)}" 
    clientSock = start_sockets(user)

    msg: str = ""

    if default_colors:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
    else:
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.nodelay(True)

    while True:
        # render
        header_pad = " " * ((curses.COLS - len("Py-chat")) // 2)
        if (len(header_pad) * 2) + len("Py-chat") != curses.COLS:
            trailing = " "
        else:
            trailing = ""

        stdscr.addstr(
            0,
            0,
            header_pad + "Py-chat" + header_pad + trailing,
            curses.A_REVERSE,
        )
        stdscr.clrtobot()

        display_messages: list[str] = history[
            : max(len(history), curses.LINES - 4)
        ]
        for name, content in [
            msg.split(":", maxsplit=1) for msg in display_messages
        ]:
            stdscr.addstr(name, curses.color_pair(1))
            stdscr.addstr(":" + content + "\n")

        stdscr.addstr(curses.LINES - 3, 0, "-" * (curses.COLS - 1))
        stdscr.addstr(curses.LINES - 2, 0, "> ")
        stdscr.addstr(msg)
        stdscr.move(curses.LINES - 2, 2 + len(msg))

        # input
        try:
            char = stdscr.get_wch()
        except curses.error:
            char = 0
            time.sleep(0.1)
            stdscr.refresh()
        except KeyboardInterrupt:
            # If you quit with ctrl+c
            break

        if char and isinstance(char, str) and char.isprintable():
            msg += char
        elif char == curses.KEY_BACKSPACE or char == "\x7f":
            msg = msg[:-1]
        elif char == "\n":
            if msg.lower() == "q":
                clientSock.shutdown(socket.SHUT_RDWR)
                clientSock.close()
                break

            clientSock.send(f"{user}: {msg}".encode("utf-8"))
            msg = ""
        elif char == curses.KEY_RESIZE:
            curses.resizeterm(curses.LINES, curses.COLS)
        elif char == 0:
            continue
        else:
            raise AssertionError(char)

    return 0
