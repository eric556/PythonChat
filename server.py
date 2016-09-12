import socket
import sys
import _thread

#yay colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = int(input("port number: "))
serverSocket.bind((host,port))
serverSocket.listen(5)

serverSedSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSedSocket.connect((host, port))
nickname = bcolors.WARNING + "SERVER BROADCAST" + bcolors.ENDC

print(str(serverSocket.getsockname()))
clientList = []
clentNames = []
clientNumber = 0


#Creating some functions and threads to allow the server to speak to everyone else
def clientsend(s):
    s.sendto(nickname.encode(), (host, port))
    while True:
        msg = input()
        s.sendto(msg.encode(), (host, port))
        if msg == 'EXIT':
            global connected
            connected = False
            sys.exit(0)

try:
    _thread.start_new_thread(clientsend, (serverSedSocket,))
except:
    print("unable to start thread")

#setting up all the threads and functions the server needs to run
def recv(s, nickName):
    while True:
        try:
            data = s.recv(1024)
            if not data: sys.exit(0)
            print(str(s.getpeername()) + ": " + data.decode())
            sendall(( bcolors.OKBLUE + nickName + bcolors.ENDC + ": " + data.decode()).encode(), s)

            if data.decode() == 'EXIT':
                connected = False
                sys.exit(0)
        except socket.error:
            print("somthing went wrong with reciving data from: %s. Maybe it was a disconnect" % str(s.getpeername()))
            sendall(("%s left the chat room" % nickName).encode(), s)
            s.close()
            clientList.remove(s)


def sendall(msg, sender):
    for s in clientList:
        if sender == None or str(sender.getpeername()) != str(s.getpeername()):
            s.sendto(msg, (s.getsockname()))

def send():
    msg = input()
    for s in clientList:
        s.sendto((bcolors.WARNING + "SERVER BROADCAST: " + bcolors.ENDC + msg).encode(), (s.getsockname()))


def connectnewclient(s,clientNickName):
    global clientNumber
    clientNumber += 1
    print(clientNumber)
    clientList.append(s)
    try:
        _thread.start_new_thread(recv, (s,clientNickName,))

    except:
        print("unable to start thread for connection: " + str(clientNickName))



while True:
    try:
        clientSocket, addr = serverSocket.accept()

    except:
        print("something went wrong")

    clientNickName = (clientSocket.recv(1024)).decode()
    clentNames.append(clientNickName)
    sendall(("%s just joined the chat room" % clientNickName).encode(), clientSocket)
    _thread.start_new_thread(connectnewclient, (clientSocket, clientNickName,))






