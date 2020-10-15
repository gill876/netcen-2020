# Client to implement simplified 'secure' electronic voting algorithm
# and send votes to a server

# Author: 
# Last modified: 2020-10-07
# Version: 0.1.1
#!/usr/bin/python3

from socket import socket, AF_INET, SOCK_STREAM
import random
import math
import sys
import json
import time

class NumTheory:
    
    @staticmethod
    def expMod(b,n,m):
        """Computes the modular exponent of a number"""
        """returns (b^n mod m)"""
        if n==0:
            return 1
        elif n%2==0:
            return NumTheory.expMod((b*b)%m, n/2, m)
        else:
            return(b*NumTheory.expMod(b,n-1,m))%m
	
class PaillierClientSocket:

    def __init__(self, host, port):
        # Add code to initialize this class.
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((host, port))
        
    def ProcessMsgs(self):
        """Main event processing method"""
        msg_lst = self.data.split(" ")
        code = ''
        try:
            code, rest = int(msg_lst[0]), msg_lst[1]
        except Exception as e:
            print(e)

        if code == 105:
            return 1

        elif code == 106:
            rest = json.loads(self.data[4:])
            return 1

        elif code == 107:
            return 1

        else:
            print("Closing Client")
            return 0

    def mysend(self, msg):
        """Add code here to send message into the socket"""
        self.s.send(msg.encode('utf-8'))
        print(f"\nSent: \"{msg}\"")
    
    def myreceive(self):
        """Add code here to read data from the socket"""
        self.data = self.s.recv(1024).decode('utf-8')
        print(
            f"\nServer msg: \"{self.data}\""
        )
    
'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print ("Please supply a server address and port.")
        sys.exit()
    serverHost = str(args[1])       # The remote host
    serverPort = int(args[2])       # The same port as used by the server

    print("Client of ____")
    c = PaillierClientSocket(serverHost, serverPort)

    c.mysend("100 Hello")

    while True:
        c.myreceive()

        msg = c.ProcessMsgs()

        if msg == 0:
            break

        elif isinstance(msg, str):
            c.mysend(msg)
            time.sleep(1)

        else:
            continue

    c.mysend("0 Welp...")
