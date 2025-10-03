from flask import Flask, request, jsonify
from collections import defaultdict
from Logger import Logger
from Logger import LogType
import geoip2.database
import sqlite3

GEO_DB_PATH = "GeoLite2-Country.mmdb"
REQ_DB_PATH = "server_data.db"
FILE_NAME = "web_server.py:"
TABLE_NAME = "geolocation"

app = Flask(__name__)
log = Logger()
cursor = None
connection = None

# In - memory data set for sorting ips by countries 
# key = country, value = list of ips that belongs to this country
country_ip_set = defaultdict(set)

# Create DB in sqlite3
def create_db():
    global cursor
    global connection

    connection = sqlite3.connect(REQ_DB_PATH, check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS geolocation (
        id INTEGER PRIMARY KEY,
        ip TEXT,
        country TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    connection.commit()

def get_country(ip: str):
    try:
        # Open the GeoLite2 database
        with geoip2.database.Reader(GEO_DB_PATH) as reader:
            response = reader.country(ip)
            return response.country.iso_code  # Returns the country code (for example: 'IL' for Israel)
    except Exception as e:
        log.add_log(f"{FILE_NAME} Error retrieving country for IP {ip}: {e}", LogType.ERROR)
        print(f"Error retrieving country for IP {ip}: {e}")
        return None

@app.route('/geo-location', methods=['POST'])
def post_geo_location():
    '''
    Function that updates the db with ip and it's location.
    '''

    data = request.json

    ip = data.get("ip")
    if not ip:
        log.add_log(f"{FILE_NAME} error: IP address is required", LogType.ERROR)
        return jsonify({"error": "IP address is required"}), 400

    country = get_country(ip) # get the country of the ip

    # Add to the db
    cursor.execute(f"INSERT INTO {TABLE_NAME} (ip, country) VALUES (?, ?)", (ip, country))
    connection.commit()

    # add to country-ip set
    country_ip_set[country].add(ip) 

    # add the action description to the log file
    log.add_log(f"{FILE_NAME} Added the ip: {ip}:{country} to the db", LogType.INFO)
    return jsonify({"ip": ip, "country": country})


@app.route('/ips', methods=['GET'])
def get_ips_by_country():
    '''
    Function that by given country returns all the ips that were queried for Geolocation.
    Support optionable datetime filters (by default returns all)
    '''

    country = request.args.get('country')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not country:
        log.add_log(f"{FILE_NAME} error: Country is required", LogType.ERROR)
        return jsonify({"error": "Country is required"}), 400

    query = f"SELECT ip FROM {TABLE_NAME} WHERE country = ?"
    params = [country]

    # Optional params
    if start_date:
        query += " AND timestamp >= ?"
        params.append(start_date)

    if end_date:
        query += " AND timestamp <= ?"
        params.append(end_date)

    cursor.execute(query, params)

    # Create list of ips 
    ips = [] 
    rows = cursor.fetchall()  # Fetch all rows from the query result
    for row in rows:
        ips.append(row[0])  

    log.add_log(f"{FILE_NAME} IPs queried for Country {country} with filters {start_date} to {end_date}",  LogType.INFO)
    return jsonify({"country": country, "ips": ips})


@app.route('/top-countries', methods=['GET'])
def top_countries():
    '''
    Returns the top 5 countries by number of Geolocation requests 
    '''

    cursor.execute(f"SELECT country, COUNT(*) as count FROM {TABLE_NAME} GROUP BY country ORDER BY count DESC LIMIT 5")
    results  = cursor.fetchall()  # Fetch all rows from the query result

    log_line = f"{FILE_NAME} top 5 countries are: "
    top_countries = []
    for country, count in results:
        country_count_line = [{"country" : country, "count" : count}]
        top_countries.append(country_count_line)

        log_line += f"Country: {country}, Count: {count}\n"
        
    log.add_log(log_line, LogType.INFO)
    return jsonify(top_countries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)