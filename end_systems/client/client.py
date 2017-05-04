import os
import sys
import random
import time

if len(sys.argv) < 4:
    print "Usage: python client.py <CLIENT_PORTS_RANGE> <PROXY_PORT> <END_SERVER_PORT>"
    print "Example: python client.py 20001-20010 20000 19990-19999"
    raise SystemExit

CLIENT_PORT = sys.argv[1]
PROXY_PORT = sys.argv[2]
SERVER_PORT = sys.argv[3]

D = {0: "GET", 1:"POST"}
time.sleep(int(random.random()%10) + 1)
while True:
    filename = "%d.data" % (int(random.random()*9)+1)
    METHOD = D[int(random.random()*len(D))]
    os.system("curl --request %s --proxy 127.0.0.1:%s --local-port %s 127.0.0.1:%s/%s" % (METHOD, PROXY_PORT, CLIENT_PORT, SERVER_PORT, filename))
    time.sleep(10)
