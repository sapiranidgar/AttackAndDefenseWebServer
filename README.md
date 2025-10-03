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
The CLI support:
-	Syn-flood
-	URL brute-force
-	An additional attack of your choice (should add)
The attacking process is capable of sending 500 requests per second.

### 3. Proxy Defense
Reverse proxy between the attacking service and the webserver.
-	The proxy detects and defends against each of the attacks from part 2
-	The proxy log all of its activities

## How to Execute the Task

1. Run the web_server.py file first to start the web server:
```python
python web_server.py
```
This will make the web server available at http://localhost:8080.

2. Run the proxy.py file to start the reverse proxy:
```python
python proxy.py
```
The proxy will forward requests to the web server and is available at http://localhost:8081.

3. Run the attack_service.py file to simulate attacks:
```python
python attack_service.py
```
You’ll be prompted to select an attack type and target.
Use the proxy address (http://localhost:8081) as the target to ensure the attacks are routed through the proxy.


## Disclamer 
This repository is for educational purpose only. Developers and contributers of this project will not be responsible for any damage caused directly or indirectly through this project.
