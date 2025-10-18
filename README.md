# AttackAndDefenseWebServer
This repository shows different attacks and their defenses on a web server using proxy.

## The task

In this repository we create a web server, attack it and use a proxy that detects the attacks on the server and defenses against them.
The task is composed of 3 main parts, where each part can be executed sollely or by running all components together:

### 1. Web Server
Small http server with an API that supports the following endpoints:
- Geolocation – given an IP returns its country
-	Given a country returns all the IPs from that location that were queried for Geolocation. Support optionable datetime filters (by default returns all)
- Top 5 countries by number of Geolocation Requests
- The server log all of its activities.

To execute the server run:

```
python server/server_main.py
```


### 2. Attack Service
Simple and understandable CLI that attacks the web server from part 1.
The CLI supports the following attacks:
-	Syn-flood (Direct and Spoofed)
-	URL brute-force
-	ICMP Smurf

The attacking process is capable of sending any number of requests.

The client can also use the web server and send valid api request supported by the server (1-3 from the server options).

To execute the client and use regular api requests (while the server is also running), you should:

1. Run the command: ```
python client/client_main.py```
2. Choose one of the options 1-3 and fill the necessary information.
3. You can choose the exit option to close the program (5).

To execute the client and attack a target point, you should:
1. Run the command: ```
python client/client_main.py```
2. Choose the option 4 from the main menu and fill the necessary information (target ip, target port, number of packets to send).
3. Choose the attack type from the attack menu (1-4). If necessary, the program will ask you to fill additional parameters.
4. You can choose the exit option to close the program (5).

### 3. Proxy Defense
Reverse proxy between the attacking service and the webserver.
The proxy is a server that listens to any received packets and transfers them to the web server while analyzing them and detecting possible attacks.
-	The proxy detects and defends against each of the attacks from part 2
-	The proxy log all of its activities

The attacks that can be detected by the proxy are:
1. syn flood (based on syn and ack count ratio).
2. url brute force (based on number of requested paths in a single time window).
3. ICMP Smurf (based on number of ECHO requests in a single time window).
4. Attempt for a regular dos attack (based of number of requests of a source in a single time window).

To execute the proxy server (who transfers messages to the web server), run:
```python
python proxy/proxy_main.py
```

## How to Execute the Entire System

1. To run the server, run the command:
```python
python server/server_main.py
```
This will make the web server available at http://localhost:8000.

2. Run the proxy.py file to start the reverse proxy:
```python
python proxy.py
```
The proxy will forward requests to the web server and is available at http://localhost:8001.

3. Run the client_main.py file to send requests to the server:
```python
python client/client_main.py
```

The available options of the client are:
- GEO-Location request.
- Get all Ips in a given country.
- Get top 5 countries.
- Attack the server.
- Exit the program.

In each choice, you will be prompted with relevant inputs necessary to complete the task.
If you choose "Attack the Server" option - choose one of the available attacks (1-4).
You'll need to enter target IP address and port in order to perform the attack.

To attack the server directly, enter the address 127.0.0.1 and port 8000 (while executing the server locally).

To attack the server through the proxy (so that the proxy could detect the attacks), enter the address 127.0.0.1 and port 8001 (while executing the server locally).

## Disclamer 
This repository is for educational purpose only. Developers and contributers of this project will not be responsible for any damage caused directly or indirectly through this project.
