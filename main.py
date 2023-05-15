import socket
import threading
import os

os.system('color A0')
os.system('cls')
choice = input("Do you Want to host(1) or to connect (2)?\t")

if choice == "1":
    server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.56.1", 9999))
    server.listen ()
    
    client, _ = server.accept()

elif choice == "2":
    client = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.56.1", 9999))

else:
    exit()


def sending_message(c):
    print("Write Your Message:")

    while True:
        
        message =input("")
        c.send(message.encode())
        print("You: "+ message )

        
def reciving_message(c):
    while True:
        print("Partner : "+ c.recv(1024).decode())

        
threading.Thread(target=sending_message, args=(client,)).start()
threading.Thread(target=reciving_message, args=(client,)).start()