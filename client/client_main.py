from client.client_executor import Client
from web_attacks.attack_type import AttackType

DEFAULT_TARGET_PORT = 8000

def print_options_to_client():
    print("Hello to GEO-Location Client!")
    print("Choose between one of the following options:")
    print("1. GEO-Location - get the country of a given ip address.")
    print("2. Get all ip addresses that made GEO-Location request to a given country.")
    print("3. Get top 5 countries with most GEO-Location requests.")
    print("4. Generate an attack.")


def print_attack_choices_to_client():
    print("choose one of the following attacks:")
    print("1. Syn-Flood attack.")
    print("2. Url-Bruteforce attack")
    print("3. Other attack")


def handle_attack(client: Client):
    print("Welcome to the Attacks menu!")
    target_address = str(input("Enter your target (IP or URL): "))
    target_port = int(input(f"Enter your target port (should be {DEFAULT_TARGET_PORT}: "))
    print_attack_choices_to_client()
    client_choice = AttackType(int(input()))
    if client_choice == AttackType.SYN_FLOOD:
        client.perform_syn_flood_attack(target_address, target_port)
    elif client_choice == AttackType.URL_BRUTE_FORCE:
        client.perform_url_brute_force_attack(target_address, target_port)
    elif client_choice == AttackType.THIRD_ATTACK:
        client.perform_third_attack(target_address, target_port)
    else:
        print("Invalid attack choice. Only 1-3 are allowed.")


def handle_country_request(client: Client):
    ip_address = input("Enter IP address to check it's country: ")
    server_result = client.send_country_request(ip_address)
    print(server_result)


def handle_all_ips_request(client: Client):
    country = input("Enter country code to receive its addresses: ")
    # todo: add date filtering
    server_result = client.send_get_all_addresses_in_country_request(country)
    print(server_result)


def handle_top_countries_request(client: Client):
    print("Retrieving top countries from the server...")
    server_result = client.send_get_top_countries_request()
    print(server_result)


def main():
    client_executor = Client()
    print_options_to_client()
    client_choice = int(input())
    if client_choice == 4:
        handle_attack(client_executor)
    elif client_choice == 1:
        handle_country_request(client_executor)
    elif client_choice == 2:
        handle_all_ips_request(client_executor)
    elif client_choice == 3:
        handle_top_countries_request(client_executor)
    else:
        print("Invalid choice. Only options 1-4 are allowed.")


if __name__ == "__main__":
    main()