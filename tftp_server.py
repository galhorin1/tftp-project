import socket
import os
import threading


# the server ip address
serverIP = "127.0.0.1"
# server active port
serverPort = 69
# the packet buffer size
bufferSize = 512
# dir for the files for reading/writing
filesDir = os.getcwd()
# change the '\\' to your operating system path separator
sep = '\\'
# free ports
portsStack = []

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip and port
UDPServerSocket.bind((serverIP, serverPort))


# reset the ports for the server to use for clients
def ports_reset():
    for i in range(10):
        portsStack.append(20000+i)


# func to send files to the client
def send_file(port):
    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip and port
    serverSocket.bind((serverIP, port))
    receive = serverSocket.recvfrom(bufferSize)
    filename1 = receive[0].decode('ascii')
    address1 = receive[1]
    filepath = filesDir + sep + filename1
    # check if the file exist
    if os.path.exists(filepath) and os.path.isfile(filepath):
        print("file exists now sending it")
        file1 = open(filepath, "r")
        msg = file1.read(bufferSize)
        # read the file and send parts of it to the client
        while msg != "":
            data = msg.encode('ascii')
            serverSocket.sendto(data, address1)
            receive = serverSocket.recvfrom(bufferSize)
            replay = receive[0].decode('ascii')
            address1 = receive[1]
            if replay == "ok":
                msg = file1.read(bufferSize)
        serverSocket.sendto("".encode('ascii'), address1)
    # if the file does not exist inform the client
    else:
        print("file does not exists ")
        data = "error file does not exist".encode('ascii')
        serverSocket.sendto(data, address1)
    portsStack.append(port)
    serverSocket.close()
    print('finished and waiting next client')


# server receiving files func
def receive_file(port):
    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((serverIP, port))
    replay = serverSocket.recvfrom(bufferSize)
    filename = replay[0].decode('ascii')
    serverSocket.sendto("ok".encode('ascii'), address)
    replay = serverSocket.recvfrom(bufferSize)
    info = replay[0].decode('ascii')
    address1 = replay[1]
    if info == "error file does not exist":
        print(info)
    else:
        filepath = filesDir + sep + filename
        file1 = open(filepath, "w")
        while info != "":
            file1.write(info)
            data2send = "ok".encode('ascii')
            serverSocket.sendto(data2send, address1)
            replay = serverSocket.recvfrom(bufferSize)
            info = format(replay[0].decode('ascii'))
            address1 = replay[1]
        file1.close()
    portsStack.append(port)
    serverSocket.close()
    print('finished and waiting next client')


ports_reset()

# server will be up and listening for clients always filtering the requests to threads
while True:
    # UDP server at port get message from the client with what the client wants to do
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    # decode client message
    clientMsg = format(message.decode('ascii'))
    if clientMsg == "Send":
        print("client requested to send files to the server")
        portUse = portsStack.pop()
        bytesToSend = str(portUse).encode('ascii')
        UDPServerSocket.sendto(bytesToSend, address)
        # create thread to listen in port and help the user with the request
        t = threading.Thread(target=receive_file, args=[portUse])
        t.run()
    elif clientMsg == "Receive":
        print("client requested to receive files from the server")
        portUse = portsStack.pop()
        bytesToSend = str(portUse).encode('ascii')
        UDPServerSocket.sendto(bytesToSend, address)
        # create thread to listen in port and help the user with the request
        t = threading.Thread(target=send_file, args=[portUse])
        t.run()
    else:
        bytesToSend = "failed".encode('ascii')
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)