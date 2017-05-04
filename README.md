# Proxy Server
An HTTP proxy server implemented via python socket programming with caching, blacklisting, authentication functionality

## Description
- ![proxy.py](/proxy.py) is the main proxy file
- Proxy runs on some specific ports, some ports are reserved for clients and some for servers
- ![end_systems](/end_systems) contains the server and the client codes
	- Client keeps asking any file [1-10].data from server by GET or POST method
	- Server listens to specified port and serves any file as asked
- Proxy works as middleman between the server and client and it does caching, authentication, etc
- Only GET and POST requests are handled

## Features
- Receives the request from client and pass it to the server after necessary parsing
- Threaded proxy server thus able to handle many requests at the same time
- If one file is requested above the threshold number of times in certain time period, then proxy server caches that request. The threshold number and time limit can be set by changing global constants in ![proxy.py](/proxy.py) file
- To maintain integrity, cached files are accessed by securing mutex locks
- Cache has limited size, so if the cache is full and proxy wants to store another response then it removes the least recently asked cached response. Cache limit can be set by setting up the constant in ![proxy.py](/proxy.py) file
- Certain servers (their ports) are blacklisted so that normal users can't access it. Blacklisted servers are stored in CIDR format in ![blacklist.txt](/blacklist.txt) file.
- Special users can access blacklisted servers. They must be authenticated by HTTP authentication. HTTP authentication is done by proxy. Usernames and passwords of priviledged users are stored in ![username_password.txt](/username_password.txt) file.

## How to run

### Proxy
- Specify proxy port while running proxy  
`python proxy.py 20000`  
It will run proxy on port 20000

### Server
- run server in ![end_systems/server](/end_systems/server) directory  
- `python server.py 19999` to run server on port 19999  
- `bash start_servers.sh 19995 19999` to run servers on all ports from 19995 to 19999.  
this script will run servers on screens
- `bash stop_servers.sh` to stop all screen processes.

### Client
- curl request can be sent as client request and get the response.  
`curl --request GET --proxy 127.0.0.1:20000 --local-port 20001-20010 127.0.0.1:19999/1.data`  
this request will ask 1.data file from server 127.0.0.1/19999 by GET request via proxy 127.0.0.1/20000 using one of the ports in range 20001-20010 on localhost.
- valid username and password should be provided to access blacklisted servers.  
`curl --request GET -u username:password --proxy 127.0.0.1:20000 --local-port 20001-20010 127.0.0.1:19998/1.data`  
- client script which randomly asks any file from any server is provided in ![end_systems/client/](end_systems/client/)  
`python client.py 20001-20010 20000 19995-19999`  
this will run a client which asks, after every 10 seconds, any file from any server in range 19995-19999, using any port in range 20001-20010, via proxy at port 20000
- In directory ![end_systems/client/](end_systems/client/)  
`bash start_clients.sh 20001 20010 20000 19995 19999`  
will run 10 client scripts each on one port in range 20001-20010, in separate screen, asking any file from any server in range 19995-19999 using proxy at port 20000
- `bash stop__clients.sh` will terminate all screens.

### Miscellaneous
- `stop__clients.sh` and `stop_servers.sh` will terminate all screens including servers and clients.
- run 5 servers, 10 clients and proxy to see the proxy's features working.  
`python proxy.py 20000`  
`bash start_servers.sh 19995 19999`  
`bash start_clients.sh 20001 20010 20000 19995 19999`  
- set blacklisted server port in ![blacklist.txt](/blacklist.txt) and username password in ![username_password.txt](/username_password.txt) and try to access blacklisted port using curl command.
- see the changes in cache directory.

## Scope of improvement
- Remove authentication headers after authentication.
- Handle HTTPS requests also.
- Try some security attacks on working proxy and give solutions to secure it.
