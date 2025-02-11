import socket
import threading

host = '127.0.0.1'
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen()
print("Server is listening...")

clients = {}


def send_all(message):
    for client in clients:
        try:
            client.send(message)
        except (ConnectionResetError, BrokenPipeError):
            print(f"Error sending message to {clients[client]}")

def send_to(target, message):
    for client in clients:
        if clients[client] == target:
            try:
                client.send(message)
            except (ConnectionResetError, BrokenPipeError):
                print(f"Error sending message to {target}")


def handle(client):
    while True:
        message = client.recv(1024).decode("utf-8")
        if message.startswith("JOIN"):
            parts = message.split(" ")
            username = parts[1]
            print("Username is:", username)
            client.send(f"Welcome {username}!".encode("utf-8"))
            send_all(f"{username} joined the chat!".encode("utf-8"))
            clients[client] = username
        elif message.startswith("LEAVE"):
            username = clients[client]
            send_all(f"{username} left the chat!".encode("utf-8"))
            del clients[client]
            client.close()
            break
        elif message.startswith("CLIENT LIST"):
            cl_str=",".join(clients.values())
            cl_list="CLIENTS CONNECTED:"+cl_str
            client.send(cl_list.encode("utf-8"))
        elif message.startswith("SEND MSG"):
            username = clients[client]
            parts = message.split("TO ")
            parts = parts[1].split(" ", 1)
            target = parts[0]
            message = parts[1]
            if target == "ALL":
                send_all(f"{username}: {message}".encode("utf-8"))
            else:
                send_to(target, f"{username}: {message}".encode("utf-8"))
        else:
            client.send("Invalid Command".encode("utf-8"))


while True:
    client, address = s.accept()
    print(f"Connected to {address}")
    client_thread = threading.Thread(target=handle, args=(client,))
    client_thread.start()
