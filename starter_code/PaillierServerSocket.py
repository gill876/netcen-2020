# Server to implement simplified 'secure' electronic voting algorithm
# and tally votes from a client.

# Author: 
# Last modified: 2020-10-07
# Version: 0.1.1
#!/usr/bin/python3

from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
import random
import math
import sys

class NumTheory:
    # def __init__(self):
    #    pass

    @staticmethod
    def expMod(b,n,m):
        """
        Computes the modular exponent of a number
        
        returns (b^n mod m)
        """
        if n==0:
            return 1
        elif n%2==0:
            return NumTheory.expMod((b*b)%m, n/2, m)
        else:
            return(b*NumTheory.expMod(b,n-1,m))%m
    
    @staticmethod
    def gcd_iter(u, v):
        """Iterative Euclidean algorithm to find the greatest common divisor of
           integers u and v
        """
        while v:
            u, v = v, u % v
        return abs(u)
    
    @staticmethod
    def lcm(u, v):
        """Returns the lowest common multiple of two integers, u and v"""
        return int((u*v)/NumTheory.gcd_iter(u, v))
    
    @staticmethod
    def ext_Euclid(m,n):
        """Extended Euclidean algorithm. It returns the multiplicative
            inverse of n mod m"""
        a = (1,0,m)
        b = (0,1,n)
        while True:
            if b[2] == 0: return a[2]
            if b[2] == 1: return int(b[1] + (m if b[1] < 0 else 0))
            q = math.floor(a[2]/float(b[2]))
            t = (a[0] - (q * b[0]), a[1] - (q*b[1]), a[2] - (q*b[2]))
            a = b
            b = t
    
    @staticmethod
    def L(x, n):
        """Function needed for unscrambling data """
        return math.floor((x-1)/n)


class PaillierServerSocket:
    
    def __init__(self, host, port):
        # Add code to initialize this class.
		# Optional: set options to reuse socket
        self.host = host
        self.port = port
        
    def ProcessMsgs(self):
        """Main event processing method"""
        pass

    def connect(self, host=None, port=None):
        # Add code to connect to a host and port

        # Use default host and port if it was not specified
        host = self.host if host is None else host
        host = self.port if port is None else port

        # Create socket
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((host, port))
    
    def mysend(self, msg):
        """Add code here to send message into the socket"""
        self.s.sendto(msg.encode('utf-8'), self.addr)
        print(f"\nSent: \"{msg}\" to \"{self.addr}\"")
    
    def myreceive(self):
        """Add code here to read data from the socket"""
        
        self.data, self.addr = s.recvfrom(1024)
        self.data = self.data.decode('utf-8')

        print(
            f"\nClient addr: \"{self.addr}\"" +
            f"\nClient msg: \"{self.data}\""
        )
        
'''
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
'''
if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print ("Please supply a server port.")
        sys.exit()
    HOST = ''                # Symbolic name meaning all available interfaces
    PORT = int(args[1])     # The port on which the server is listening
    if PORT < 1023 or PORT > 65535:
        print("Invalid port specified.")
        sys.exit()
        
    p = int(input('Enter P : ')) # 307
    q = int(input('Enter Q: ')) # 439
    n = p*q
    euler = (p-1)*(q-1)
    lAmbda = NumTheory.lcm(p-1, q-1)
    if NumTheory.gcd_iter(n, euler) != 1:
        print(str(n) + " is not relatively prime to " + str(euler))
        sys.exit()
    gen = random.randint(1,n**2)
    L_fn_input = NumTheory.expMod(gen, lAmbda, n**2)
    mu = NumTheory.ext_Euclid(n,NumTheory.L(L_fn_input,n))
    print("Public key: (" + str(n) + "," + str(gen) +")")
    print("Private key: " + str(lAmbda))
    print("mu: " + str(mu))
    
    print("Server of ____")
    s = PaillierServerSocket(HOST,PORT)
