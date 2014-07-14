import socket
import threading

""" Pharo code:
stream := SocketStream openConnectionToHostNamed: ' 127.0.0.1'  port: 5000 .
stream sendCommand: 'Hello Pharo AGAIN!!!!'.
stream close.

"""
ephestos_running = False
thread_created = False
threadSocket = 0
s = 0
receivedSocket = "none"
listening = False

def create_thread():
    print("creating thread")
    global threadSocket,listening
    threadSocket = threading.Thread(name='threadSocket', target= socket_listen)
    listening = True
    print("calling create_socket_connection")
    create_socket_connection()
    threadSocket.start()
    #threadSocket.join()

def socket_listen():
    global receivedSocket,listening,s
    loop = 1
    print("listening")

    s.listen(5)

    while listening:
        (receivedSocket , adress) = s.accept()
        print("receivedSocket:",receivedSocket)
        print("adress",adress)
        print("data : ",receivedSocket.recv(1024))

        print("----END OF LOOP-------")
        loop = loop + 1
        if loop > 5 : listening = False




def create_socket_connection():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1',5000))


def another_thread():
    for i in range(0,1000):
        print("hello there!!")

anotherThread = threading.Thread(target=another_thread)
anotherThread.start()
#anotherThread.join()
create_thread()
