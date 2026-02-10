#!/usr/bin/env python 3 

import socket
import threading
import datetime
import ssl
from tkinter import *
from tkinter.scrolledtext import ScrolledText


def send_message(event, client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()

    client_socket.sendall(f"\n{datetime.datetime.now().strftime('%m-%d %H:%M')} - {username}>{message}".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"\n{datetime.datetime.now().strftime('%m-%d %H:%M')} - {message}")
    text_widget.configure(state='disabled')
    
def receive_message (client_socket, text_widget):
    while True :
        try:
            message = client_socket.recv(1024).decode()
            print(message)
            if not message:
                break
            text_widget.configure(state='normal')
            text_widget.insert(END, message)
            text_widget.configure(state='disabled')

        except:
            break
    
def list_user_request(client_socket):
    client_socket.sendall("!users".encode())
    print(f"Mensaje !users enviado correctamente")

def exit_request(client_socket, username, window):
    try:
        client_socket.sendall("!exit".encode())
        client_socket.close()
    except:
        pass

    finally:
        window.quit()
        window.destroy()

def client_program():
    host = 'localhost'
    port = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = ssl.wrap_socket(client_socket)
    client_socket.connect((host, port))
    
    
    username = input("[+] Introduce tu user name :")
    client_socket.sendall(username.encode())

    window = Tk()
    window.title("Chat")

    text_widget = ScrolledText(window, state='disabled')
    text_widget.pack(padx=5, pady=5)

    frame_widget = Frame(window)
    frame_widget.pack(padx=5, pady=5, fill=BOTH, expand=1)

    entry_widget = Entry(frame_widget, width=30)
    entry_widget.bind("<Return>", lambda event:send_message(event, client_socket, username, text_widget, entry_widget))
    entry_widget.pack(side=LEFT, fill=BOTH, expand=1)

    button_widget = Button(frame_widget, text="Enviar", command=lambda :send_message(None, client_socket, username, text_widget, entry_widget))
    button_widget.pack(side=RIGHT, padx=5)

    users_widget = Button(window, text="Listat Usuarios", command=lambda :list_user_request( client_socket))
    users_widget.pack(padx=5, pady=5)

    exit_widget = Button(window, text="Exit", command=lambda :exit_request( client_socket, username, window))
    exit_widget.pack(padx=5, pady=5)

    thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
    thread.demon = True
    thread.start()

    window.mainloop()
  
if __name__ =='__main__':
    client_program()
