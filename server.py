import socket
import threading

host = socket.gethostbyname(socket.gethostname())
print(host)
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat')
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        clients.append(client)
        nicknames.append(nickname)

        print(f'nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat\n'.encode('ascii'))
        client.send("You joined the chat!".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("The server is started and its in listening mode....")
receive()