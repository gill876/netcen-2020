# Server to implement simplified 'secure' electronic voting algorithm
# and tally votes from a client.

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
        self.n, self.gen = None, None
        
    def ProcessMsgs(self):
        """Main event processing method"""
        msg_lst = self.data.split(" ")
        code = ''
        try:
            code, rest = int(msg_lst[0]), msg_lst[1]
        except Exception as e:
            print(e)

        if code == 100:
            msgs = []

            key = f"105 Key {self.n} {self.gen}"
            candidates = "106 " + json.dumps(self.candids)
            polls = "107 Polls Open"
            msgs = [key, candidates, polls]

            return msgs

        elif code == 115: # collect votes
            pass

        else:
            self.s.close()
            print("Closing Server")
            return [0]

    def connect(self, host=None, port=None):
        # Add code to connect to a host and port

        # Use default host and port if it was not specified
        host = self.host if host is None else host
        port = self.port if port is None else port

        # Create socket
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(2)

        self.conn, self.addr = self.s.accept()
    
    def mysend(self, msg):
        """Add code here to send message into the socket"""
        self.conn.send(msg.encode('utf-8'))
        print(f"\nSent: \"{msg}\" to \"{self.addr}\"")
    
    def myreceive(self):
        """Add code here to read data from the socket"""
        
        self.data = self.conn.recv(1024).decode('utf-8')

        print(
            f"\nClient addr: \"{self.addr}\"" +
            f"\nClient msg: \"{self.data}\""
        )

    def addCandid(self, candidates):
        self.candids = candidates
        
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
    s.gen = str(gen)
    s.n = str(n)

    s.connect()
    candidates = [{"ID": 2**8, "Candidate": "John Brown"}, {"ID": 2**16, "Candidate": "Mary Black"}]
    s.addCandid(candidates)

    while True:
        s.myreceive()
        msg = s.ProcessMsgs()

        for m in msg:
            if m == 0:
                break
            s.mysend(m)
            time.sleep(1)
