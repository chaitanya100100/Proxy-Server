import thread
import socket
import sys
import os
import datetime


# global variables
max_connections = 10
BUFFER_SIZE = 4096


# take command line argument
if len(sys.argv) != 2:
    print "Usage: python %s <PROXY_PORT>" % sys.argv[0]
    print "Example: python %s 20000" % sys.argv[0]
    raise SystemExit

try:
    proxy_port = int(sys.argv[1])
except:
    print "provide proper port number"
    raise SystemExit


# A thread function to handle one request
def handle_one_request_(client_socket, client_addr, client_data):
    client_socket.send(client_data)
    client_socket.close()


# This funciton initializes socket and starts listening.
# When connection request is made, a new thread is created to serve the request
def start_proxy_server():

    # Initialize socket
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.bind(('', proxy_port))
        proxy_socket.listen(max_connections)

        print "Serving proxy on %s port %s ..." % (
            str(proxy_socket.getsockname()[0]),
            str(proxy_socket.getsockname()[1])
            )

    except Exception as e:
        print "Error in starting proxy server ..."
        print e
        proxy_socket.close()
        raise SystemExit


    # Main server loop
    while True:
        try:
            client_socket, client_addr = proxy_socket.accept()
            client_data = client_socket.recv(BUFFER_SIZE)

            print "%s - - [%s] \"%s\"" % (
                str(client_addr),
                str(datetime.datetime.now()),
                client_data.splitlines()[0]
                )

            thread.start_new_thread(handle_one_request_, (client_socket, client_addr, client_data))
            # client_socket.send(client_data)
            # client_socket.close()
        except KeyboardInterrupt:
            proxy_socket.close()
            print "\nProxy server shutting down ..."
            break

start_proxy_server()
