from socket import *
import sys
import os
from _thread import *
import argparse
# globas vars
state = False
sock = socket()


# Infinite loop to keep client running.
def clientthread():
    global state
    while True:
        try:
            data = sock.recv(1024)
            if data: print(data.decode().rstrip())
        except:
            # Clean up the connection
            state = True
            sock.close()
            break
def main():
    # try:
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action="store", dest="host", required=False)
    parser.add_argument('--port', action="store", dest="port", type=int, required=False)
    # get params
    args = parser.parse_args()
    host = args.host if args.host else '127.0.0.1'
    port = args.port if args.port else 8000
    print ((host,port))

    # Connect takes tuple of host and port
    sock.connect((host, port))
    while True:
        start_new_thread(clientthread, ())
        try:
            sys.stdout.flush()
            msg = sys.stdin.readline()
            sock.send(msg.rstrip().encode())
        except:
            # alert error in connection
            if state:
                print("Error: The server was disconnected.")
            break
    # except:
    #     print("Error: You cannot connect to the server.")
    #     exit()
main()