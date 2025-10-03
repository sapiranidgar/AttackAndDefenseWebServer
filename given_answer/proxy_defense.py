from flask import Flask, request, Response, current_app
from datetime import datetime, timedelta
from collections import Counter
from web_server import log
from Logger import LogType
import requests


FILE_NAME = "proxy_defense.py:"

proxy_app = Flask(__name__)

# Rate-limiting variables
request_counts = Counter()
banned_ips = set()
threshold = 100  # Max requests per time window
window = timedelta(seconds=10)

@proxy_app.before_request
def filter_requests():
    """
    Filter and block requests based on rate-limiting criteria
    """

    client_ip = request.remote_addr
    now = datetime.now()

    to_remove = []
    for ip, count_time in request_counts.items():
        # if the request is old enough we can remove it
        if now - count_time[1] > window:
            to_remove.append(ip)
    
    # Delete the old request counts
    for ip in to_remove:
        del request_counts[ip] 

    # If the client is already banned, block the request
    if client_ip in banned_ips:
        log.add_log(f"{FILE_NAME} the ip:{client_ip} is on the banned list, request is blocked", LogType.ERROR)
        return Response("Blocked", status=403)
    
    # If the client is new, init count
    if client_ip not in request_counts:
        request_counts[client_ip] = [1, now]
    else: # the client is not new, increase the count
         request_counts[client_ip][0] += 1

    # If the IP exceeds the allowed threshold, ban it
    if request_counts[client_ip][0] > threshold:
        banned_ips.add(client_ip)  # Add the IP to the banned list
        log.add_log(f"Banned IP {client_ip} for exceeding request threshold", LogType.WARNING)


@proxy_app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@proxy_app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    """
    Forwards requests to the target server
    """

    if request.host == "localhost:5000":  # Adjust this to the proxy's host and port
        log.add_log(f"Blocked: Attempt to self-proxy", LogType.WARNING)
        return Response("Blocked: Attempt to self-proxy", status=400)
    
    target_url = f"http://localhost:8080/{path}"  # The target server's URL
    
    try:
        # Send the received request to the target server
        with current_app.test_client() as client:
            response = client.open(
                path=f"/{path}",
                method=request.method,
                headers={key: value for key, value in request.headers},
                data=request.get_data()
            )

        log.add_log(f"Proxy passed request to {target_url}", LogType.INFO)
        # Return response from the target server
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        headers = []
        for name, value in response.headers.items():
            if name.lower() not in excluded_headers:
                headers.append((name, value))
        
        return Response(response.data, status=response.status_code, headers=headers)

    except Exception as e:
        log.add_log(f"Proxy failed to forward request to {target_url}: {e}", LogType.ERROR)
        return Response(f"Error while forwarding request: {e}", status=500)
    

if __name__ == "__main__":
    proxy_app.run(host="127.0.0.1", port=8081)