import socket
import sys
import _thread

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = int(input("port number: "))
serverSocket.bind((host,port))
serverSocket.listen(5)

print(str(serverSocket.getsockname()))
clientList = []
clentNames = []
clientNumber = 0


def recv(s, nickName):
    while True:
        try:
            data = s.recv(1024)
            if not data: sys.exit(0)
            print(str(s.getpeername()) + ": " + data.decode())
            sendall((nickName + ": " + data.decode()).encode(), s)

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
        if str(sender.getpeername()) != str(s.getpeername()):
            s.sendto(msg, (s.getsockname()))


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
    _thread.start_new_thread(connectnewclient, (clientSocket,clientNickName,))





