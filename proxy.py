import thread
import socket
import sys
import os
import datetime
import json


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


# returns a dictionary of details
def parse_details(client_addr, client_data):
    try:
        lines = client_data.splitlines()
        first_line_tokens = lines[0].split()
        url = first_line_tokens[1]

        url_pos = url.find("://")
        if url_pos != -1:
            protocol = url[:url_pos]
            url = url[(url_pos+3):]
        else:
            protocol = "http"

        port_pos = url.find(":")
        path_pos = url.find("/")
        if path_pos == -1:
            path_pos = len(url)


        if port_pos==-1 or path_pos < port_pos:
            server_port = 80
            server_url = url[:path_pos]
        else:
            server_port = int(url[(port_pos+1):path_pos])
            server_url = url[:port_pos]

        first_line_tokens[1] = url[path_pos:]
        lines[0] = ' '.join(first_line_tokens)
        client_data = "\r\n".join(lines) + '\r\n\r\n'

        return {
            "server_port" : server_port,
            "server_url" : server_url,
            "client_data" : client_data,
            "protocol" : protocol,
        }

    except Exception as e:
        print e
        print
        return None


# get the response from server and give it to client
def serve(client_socket, client_addr, details):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((details["server_url"], details["server_port"]))
        server_socket.send(details["client_data"])
        print details["client_data"]

        while True:
            reply = server_socket.recv(BUFFER_SIZE)
            if len(reply):
                client_socket.send(reply)
                #print "data : %s" % reply
            else:
                break

        server_socket.close()
        client_socket.close()
        return

    except Exception as e:
        server_socket.close()
        client_socket.close()
        print e
        return


# A thread function to handle one request
def handle_one_request_(client_socket, client_addr, client_data):

    details = parse_details(client_addr, client_data)
    if not details:return
    serve(client_socket, client_addr, details)




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

        except KeyboardInterrupt:
            proxy_socket.close()
            print "\nProxy server shutting down ..."
            break

start_proxy_server()
