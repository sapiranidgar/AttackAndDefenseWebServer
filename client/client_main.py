from client.client_executor import Client

if __name__ == "__main__":
    client = Client()
    res = client.send_country_request("182.54.23.82")
    print(res)
    res = client.send_get_all_addresses_in_country_request("US")
    print(res)
    res = client.send_get_top_countries_request()
    print(res)