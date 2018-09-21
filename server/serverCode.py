# Libraries
import socket
import sys
import os
import psutil
from _thread import *
import argparse
import sys
sys.path.append('../')
from server.configTimezone.timezone import *

connections = []

# class connection
class Connection:
    def __init__(self, conn, address):
        self.conn = conn
        self.address = address

def removeConnection(conn):
    for connection in connections:
        if connection.conn is conn:
            connections.remove(connection)
    print("Quantity of clients: " + str(len(connections)))
def nameHostServer(address,conn):
    print("Send server name to: " + address[0] + ":" + str(address[1]))
    conn.sendall(socket.gethostname().encode())

def ipServer(address,conn):
    print("Send server IP to: " + address[0] + ":" + str(address[1]))
    conn.sendall(socket.gethostbyname(socket.gethostname()).encode())

def quantityProcesses(address,conn):
    print("Send quantity of processes in the server to: " + address[0] + ":" + str(address[1]))
    conn.sendall(str(len(psutil.pids())).encode())

def countryTimezone(address, conn,country):
    time=getCountryTime(country)
    if time:
        print("Send country time to: " + address[0] + ":" + str(address[1]))
        conn.sendall(str(time).encode())
    else:
        conn.sendall("Error: Country not found".encode())

def errorCommand(address,conn):
    print("Send error command to: " + address[0] + ":" + str(address[1]))
    conn.sendall("Error: Command not found.".encode())

def replicateToClient(conn,address,data):
    for obj in connections:
        if obj.conn is not conn:
            msj = address[0] + ":" + str(address[1]) + ": " + data.decode()
            obj.conn.sendall(msj.encode())
def clientThread(conn, address):
    # infinite loop so that function do not terminate and thread do not end.
    while True:
        # 1024 stands for bytes of data to be received
        try:
            data = conn.recv(1024)
            if "-" in data.decode()[0]:
                try:
                    commandComponents = data.decode().strip("-").split(" ")
                    commandLen = len(commandComponents)
                    if commandLen == 1:
                        specificCommand=commandComponents[0]
                        if specificCommand == "nameserver":
                            nameHostServer(address, conn)
                        elif specificCommand == "ipserver":
                            ipServer(address, conn)
                        elif specificCommand == "processes":
                            quantityProcesses(address, conn)
                        else:
                            raise Exception()
                    elif (commandLen > 1 )and (commandComponents[0] == "country"):
                        countryTimezone(address, conn,' '.join(commandComponents[1:]))
                    else:
                        raise Exception()
                except Exception:
                    errorCommand(address, conn)
            else:
                if data:
                    replicateToClient(conn,address, data)
                    print("Receive data from: " + address[0] + ":" + str(address[1])+" message:"+data.decode())
        except:
            # Remove connection of the client disconnected
            removeConnection(conn)
            # Clean up the connection
            conn.close()
            break
def main():
    try:
        # params
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', action="store", dest="host", required=False)
        parser.add_argument('--port', action="store", dest="port", type=int, required=False)
        # get params
        args = parser.parse_args()
        host = args.host if args.host else ''
        port = args.port if args.port else 8000
        # Creating socket object
        sock = socket.socket()
        # Binding socket to a address. bind() takes tuple of host and port.
        sock.bind((host, port))
        # Listening at the address
        sock.listen(10)
        print("Server socket started in " + str(host) + ":" + str(port))
        while True:
            connection, address = sock.accept()
            connections.append(Connection(connection, address))
            connection.sendall("Connected to the server".encode())
            print("Quantity of clients: " + str(len(connections)))
            start_new_thread(clientThread, (connection, address))
    except:
        print("Error: The server cannot be started")

main()