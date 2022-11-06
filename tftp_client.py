import socket
import os

# initial client message
msgFromClient = "None"
serverIP = "127.0.0.1"
# server address and port
serverAddressPort = (serverIP, 69)
# buffer size
bufferSize = 512
# path for user files folder
clientFiles = os.getcwd()
# change the '\\' to your operating system path separator
sep = '\\'


# func to send files to the server
def sending_file(filename, port1):
    address = (serverIP, port1)
    data = filename.encode('ascii')
    sendSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sendSocket.sendto(data, address)
    filepath = clientFiles + sep + filename
    if os.path.exists(filepath) and (os.path.isfile(filepath)):
        print("file exists now sending it")
        file1 = open(filepath, "r")
        content = file1.read(bufferSize)
        # read the file and send parts of it to the client
        while content != "":
            data = content.encode('ascii')
            sendSocket.sendto(data, address)
            receive = sendSocket.recvfrom(bufferSize)
            replay = receive[0].decode('ascii')
            if replay == "ok":
                content = file1.read(bufferSize)
        sendSocket.sendto("".encode('ascii'), address)
    # if the file does not exist inform the client
    else:
        print("file does not exists ")
        data = "error file does not exist".encode('ascii')
        sendSocket.sendto(data, address)


# func to receive file from the server
def receive_file(filename, port1):
    address = (serverIP, port1)
    data = filename.encode('ascii')
    recSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    recSocket.sendto(data, address)
    # get replay from the server if the file exist or the first part of the file
    data = recSocket.recvfrom(bufferSize)
    info = format(data[0].decode('ascii'))
    # if the file does not exist inform the user and exit
    if info == "error file does not exist":
        print("file does not exist in server")
    # if the file exist start receiving it
    else:
        print('receiving file')
        file1 = open(clientFiles + sep + filename, "w")
        while info != "":
            file1.write(info)
            data2send = "ok".encode('ascii')
            recSocket.sendto(data2send, address)
            data = recSocket.recvfrom(bufferSize)
            info = format(data[0].decode('ascii'))
        file1.close()
    print('finished')
    exit(0)


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# what does the user want to do receive file or send one ?
print("Press 1 to send file to the server,press 2 to receive file from the server")
requestType = input("press anything else to quit : \n")
if requestType == '1':
    msgFromClient = "Send"
    fileNameSend = input("please enter file name to send\n")
    # inform server of sending intention
    bytesToSend = msgFromClient.encode('ascii')
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = format(msgFromServer[0].decode('ascii'))
    # if the server replays with port use the sending
    # file func to send the file and send the file name requested to the server
    if 20000 < int(msg) < 20010:
        port = int(msg)
        sending_file(fileNameSend, port)
    else:
        print("failed to connect to the server please try again later")
        exit(0)
elif requestType == '2':
    msgFromClient = "Receive"
    fileNameRec = input("please enter file name to receive \n")
    # inform server of Receiving intention
    bytesToSend = msgFromClient.encode('ascii')
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = format(msgFromServer[0].decode('ascii'))
    # if the server replays with ok use the receiving
    # file func to receive the file and send the file name requested from the server
    if int(msg) > 0:
        port = int(msg)
        receive_file(fileNameRec, port)
    else:
        print("failed to connect to the server please try again later")
        exit(0)
else:
    print("system will now exit")
    exit(0)
