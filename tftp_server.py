import socket
import os

# the server ip address
serverIP = "127.0.0.1"
# server active port
serverPort = 20003
# the packet buffer size
bufferSize = 512
# dir for the files for reading/writing
filesDir = os.getcwd()
# change the '\\' to your operating system path separator
sep = '\\'

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip and port
UDPServerSocket.bind((serverIP, serverPort))


# func to send files to the client
def send_file(filename1, address1):
    print("in sending func")
    filepath = filesDir + sep + filename1
    # check if the file exist
    if os.path.exists(filepath) and os.path.isfile(filepath):
        print("file exists now sending it")
        file1 = open(filepath, "r")
        msg = file1.read(bufferSize)
        # read the file and send parts of it to the client
        while msg != "":
            data = msg.encode('ascii')
            UDPServerSocket.sendto(data, address1)
            receive = UDPServerSocket.recvfrom(bufferSize)
            replay = receive[0].decode('ascii')
            address1 = receive[1]
            if replay == "ok":
                msg = file1.read(bufferSize)
        UDPServerSocket.sendto("".encode('ascii'), address1)
    # if the file does not exist inform the client
    else:
        print("file does not exists ")
        data = "error file does not exist".encode('ascii')
        UDPServerSocket.sendto(data, address1)
    print('finished and waiting next client')


# server receiving files func
def receive_file(filename1, address1):
    print("in receiving func")
    data = "ok".encode('ascii')
    UDPServerSocket.sendto(data, address1)
    replay = UDPServerSocket.recvfrom(bufferSize)
    info = replay[0].decode('ascii')
    address1 = replay[1]
    if info == "error file does not exist":
        print(info)
    else:
        filepath = filesDir + sep + filename1
        file1 = open(filepath, "w")
        while info != "":
            file1.write(info)
            data2send = "ok".encode('ascii')
            UDPServerSocket.sendto(data2send, address1)
            replay = UDPServerSocket.recvfrom(bufferSize)
            info = format(replay[0].decode('ascii'))
            address1 = replay[1]
        file1.close()
    print('finished and waiting next client')


# server will be up and listening for clients always
while True:
    # UDP server at port get message from the client with what the client wants to do
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    # decode client message
    clientMsg = format(message.decode('ascii'))
    print(clientMsg)
    if clientMsg == "Send":
        print("client requested to send files to the server")
        bytesToSend = "ok".encode('ascii')
        UDPServerSocket.sendto(bytesToSend, address)
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        # call receiving func
        receive_file(format(message.decode('ascii')), address)
    elif clientMsg == "Receive":
        print("client requested to receive files from the server")
        bytesToSend = "ok".encode('ascii')
        UDPServerSocket.sendto(bytesToSend, address)
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        # call sending func
        send_file(format(message.decode('ascii')), address)
    else:
        bytesToSend = "failed".encode('ascii')
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
