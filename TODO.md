# Definition of Done:
    - We can send and receive messages over a UDP connection
        - serverless
    - We can set our nickname - by default it uses $USER
    - Sent and recieved messages are stored in a "session" file
        - possibly json, or sqlite?
    - The TUI will show you all connected users to the left
    - The TUI will give you a message box to send a message and
        display all other messages in the current session
    - The code is unit tested to a reasonable level
        (doesn't need 100% coverage, but make sure there are some
        tests using pytest)
    - The code is fully typed and uses mypy to type-check
    - Tests run through github actions CI

### Technologies/Libs?
    [socket](https://docs.python.org/3/library/socket.html)
    [pytest](https://docs.pytest.org/en/7.4.x/)
    [textual](https://github.com/Textualize/textual)

    - Standard virtualenvs
