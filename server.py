#!/usr/bin/env python3

import socket
import threading
import ssl

def client_thread(client_socket, clients, usernames):
    username = client_socket.recv(1024).decode()
    #print(username)

    usernames[client_socket] = username
    
    for client in clients :
        if client is not client_socket :
            client.sendall(f"\n[+] EL usuario {username} se ha conectado ".encode())

    while True :
        try:
            messsage = client_socket.recv(1024).decode()

            if not messsage:
                break

            
            if messsage == "!users":

                client_socket.sendall(f"\n[+] Listados de usuarios conectados : {' ,' . join(usernames.values())} ".encode())

            if messsage == "!exit":
                messsage = ""
                for client in clients :
                    if client is not client_socket :
                        client.sendall(f"\n[+] EL usuario {username} se ha deconectado ".encode())

                client_socket.close()
                clients.remove(client_socket)
                del usernames[client_socket]
                

            for client in clients :
                if client is not client_socket :
                    client.sendall(messsage.encode())


        except:
            break;

def server_program():
    host = 'localhost'
    port = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket = ssl.wrap_socket(server_socket, keyfile="server-key.key", certfile="server-cert.pem", server_side=True)
    server_socket.listen()

    print(f"\n[+] El servidor está en escucha de conexiones entrantes ....")

    clients = []
    usernames = {}

    while True :
        client_socket, address = server_socket.accept()
        clients.append(client_socket)

        print(f"\n[+] Se ha conectado un nuevo cliente : {address}")

        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames))
        thread.demon = True
        thread.start()

    server_socket.close


if __name__ == "__main__" :
    server_program()
