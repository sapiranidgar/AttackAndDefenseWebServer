# AttackAndDefenseWebServer
This repository shows different attacks and their defenses on a web server using proxy.

## The task

In this repository we create a web server, attack it and use a proxy that detects the attacks on the server and defenses against them.
The task is composed of 3 main parts:

### 1. Web Server
Small http server with an API that supports the following endpoints:
- Geolocation – given an IP returns its country
-	Given a country returns all the IPs from that location that were queried for Geolocation. Support optionable datetime filters (by default returns all)
- Top 5 countries by number of Geolocation Requests
- The server log all of its activities.


### 2. Attack Service
Simple and understandable CLI that attacks the web server from part 1.
The CLI supports the following attacks:
-	Syn-flood (Direct and Spoofed)
-	URL brute-force
-	ICMP Smurf

The attacking process is capable of sending any number of requests.

### 3. Proxy Defense
Reverse proxy between the attacking service and the webserver.
-	The proxy detects and defends against each of the attacks from part 2
-	The proxy log all of its activities

## How to Execute the Task

1. To run the server, run the command:
```python
python server/server_main.py
```
This will make the web server available at http://localhost:8000.

2. Run the proxy.py file to start the reverse proxy:
```python
python proxy.py
```
The proxy will forward requests to the web server and is available at http://localhost:8081.

3. Run the client_main.py file to send requests to the server:
```python
python client/client_main.py
```

The available options are:
- GEO-Location request.
- Get all Ips in a given country.
- Get top 5 countries.
- Attack the server.
- Exit the program.

In each choice, you will be prompted with relevant inputs necessary to complete the task.
If you choose "Attack the Server" option - choose one of the available attacks (1-4).
You'll need to enter target IP address and port in order to perform the attack.

To attack the server directly, enter the address 127.0.0.1 and port 8000 (while executing the server locally).

## Disclamer 
This repository is for educational purpose only. Developers and contributers of this project will not be responsible for any damage caused directly or indirectly through this project.
