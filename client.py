import socket
import sys
import _thread

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("server address: ")
port = int(input("server port: "))
nickname = input("Nickname: ")
clientSocket.connect((host, port))

connected = True


def recv(s):
    while True:
        data = s.recv(1024)
        if not data:
            sys.exit(0)
        print(data.decode())


def send(s):
    s.sendto(nickname.encode(), (host, port))
    while True:
        msg = input()
        s.sendto(msg.encode(), (host, port))
        if msg == 'EXIT':
            global connected
            connected = False
            sys.exit(0)


try:
    _thread.start_new_thread(recv, (clientSocket,))
    _thread.start_new_thread(send, (clientSocket,))
except:
    print("unable to start thread")

while connected:
    pass

clientSocket.close()
