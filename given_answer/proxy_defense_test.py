import pytest
from proxy_defense import proxy_app
from flask import Response
import subprocess
import time

@pytest.fixture(scope="module")
def start_web_server():
    """Fixture to start the web server before tests."""
    # Start the Flask web server in the background
    server_process = subprocess.Popen(['python', 'web_server.py'])

    # Give the server some time to start up
    time.sleep(2)

    # Yield control back to pytest for the tests
    yield

    # After tests complete, stop the server
    server_process.terminate()
    server_process.wait()

@pytest.fixture
def client():
    with proxy_app.test_client() as client:
        yield client

def test_proxy_rate_limiting(client):
    # Send requests from a mock IP (can use any IP)
    for _ in range(110):  # Exceed the threshold of 100 requests
        response = client.get('/')
    # Expect the 403 Forbidden response after exceeding threshold
    response = client.get('/')
    assert response.status_code == 403
    assert response.data == b'Blocked'
