import pytest
from web_server import app, create_db
import json
import sqlite3
from datetime import datetime

# Fixture to setup the database
@pytest.fixture(scope="module")
def setup_db():
    # Create the database and populate it with test data
    create_db()

    # Define countries and their IPs for testing
    countries = ['US', 'IN', 'CN', 'GB', 'DE', 'BR', 'AU', 'FR']
    ip_addresses = {
        'US': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5'],
        'IN': ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5'],
        'CN': ['172.16.0.1', '172.16.0.2', '172.16.0.3', '172.16.0.4', '172.16.0.5'],
        'GB': ['80.0.0.1', '80.0.0.2', '80.0.0.3', '80.0.0.4', '80.0.0.5'],
        'DE': ['5.5.5.1', '5.5.5.2', '5.5.5.3', '5.5.5.4', '5.5.5.5'],
        'BR': ['189.0.0.1', '189.0.0.2', '189.0.0.3', '189.0.0.4', '189.0.0.5'],
        'AU': ['123.0.0.1', '123.0.0.2', '123.0.0.3', '123.0.0.4', '123.0.0.5'],
        'FR': ['192.0.0.1', '192.0.0.2', '192.0.0.3', '192.0.0.4', '192.0.0.5']
    }

    # Connect to the database
    connection = sqlite3.connect('server_data.db')
    cursor = connection.cursor()

    # Insert 50 entries into the geolocation table
    for country, ips in ip_addresses.items():
        for ip in ips:
            for _ in range(5):  # 5 entries per country
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(f"INSERT INTO geolocation (ip, country, timestamp) VALUES (?, ?, ?)", (ip, country, timestamp))

    # Commit and close the connection
    connection.commit()
    connection.close()

    yield  # Teardown after the test

# Fixture to initialize the Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test POST /geo-location endpoint
def test_post_geo_location(client, setup_db):
    # Test for valid IP
    response = client.post('/geo-location', json={"ip": "8.8.8.8"})
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert "ip" in json_data
    assert "country" in json_data

    # Test for missing IP
    response = client.post('/geo-location', json={})
    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert json_data["error"] == "IP address is required"

# Test GET /ips?country={country} endpoint
def test_get_ips_by_country(client, setup_db):
    # Test for country 'US'
    response = client.get('/ips?country=US')
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert isinstance(json_data['ips'], list)

    # Test for country 'IN'
    response = client.get('/ips?country=IN')
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert isinstance(json_data['ips'], list)

# Test GET /top-countries endpoint
def test_top_countries(client, setup_db):
    response = client.get('/top-countries')
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert isinstance(json_data, list)
    assert len(json_data) == 5  # Should return top 5 countries
