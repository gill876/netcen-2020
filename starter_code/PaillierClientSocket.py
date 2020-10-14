# Client to implement simplified 'secure' electronic voting algorithm
# and send votes to a server

# Author: 
# Last modified: 2020-10-07
# Version: 0.1.1
#!/usr/bin/python3

import socket
import random
import math
import sys

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
        pass
        
    def ProcessMsgs(self):
        """Main event processing method"""
        pass

    def mysend(self, msg):
        """Add code here to send message into the socket"""
        pass
    
    def myreceive(self):
        """Add code here to read data from the socket"""
        pass
    
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
