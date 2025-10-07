from client.client_controller import ClientController
from web_attacks.attack_type import AttackType

DEFAULT_TARGET_PORT = 8000
GOODBYE_CHOICE = 5
client_controller = ClientController()


def print_options_to_client():
    print("\n\nChoose between one of the following options:")
    print("1. GEO-Location - get the country of a given ip address.")
    print("2. Get all ip addresses that made GEO-Location request to a given country.")
    print("3. Get top 5 countries with most GEO-Location requests.")
    print("4. Generate an attack.")
    print("5. Exit the program.")


def print_attack_choices_to_client():
    print("choose one of the following attacks:")
    print("1. Syn-Flood Direct attack.")
    print("2. Syn-Flood Spoofed attack.")
    print("3. Url-Bruteforce attack")
    print("4. ICMP Smurf attack")


def handle_syn_flood_attack(target_address: str, target_port: int, number_of_packets: int, attack_type: AttackType):
    print("~~~ Starting SYN-FLOOD Attack ~~~")
    res = client_controller.perform_syn_flood_attack(target_address, target_port, attack_type,
                                                     number_of_packets)
    if res.is_successful() and res.get_data():
        print("~~~ Finished SYN-FLOOD Attack ~~~")
    else:
        print(res.get_error_msg())


def handle_url_brute_force_attack(target_address: str, target_port: int, number_of_packets: int):
    print("~~~ Starting URL Brute Force Attack ~~~")
    res = client_controller.perform_url_brute_force_attack(target_address, target_port, number_of_packets)
    if res.is_successful() and res.get_data():
        print("~~~ Finished URL Brute Force Attack ~~~")
    else:
        print(res.get_error_msg())


def handle_icmp_smurf_attack(target_address: str, number_of_packets: int):
    print("~~~ Starting ICMP-Smurf Attack ~~~")
    res = client_controller.perform_icmp_smurf_attack(target_address, number_of_packets)
    if res.is_successful() and res.get_data():
        print("~~~ Finished ICMP-Smurf Attack ~~~")
    else:
        print(res.get_error_msg())


def handle_attack():
    print("Welcome to the Attacks menu!")
    target_address = str(input("Enter your target (IP): "))
    target_port = int(input(f"Enter your target port (should be {DEFAULT_TARGET_PORT}): "))
    number_of_packets = int(input("Enter number of packets to send to target: "))
    print_attack_choices_to_client()
    client_choice = AttackType(int(input()))

    attack_details_res = client_controller.get_attack_details(client_choice)
    if attack_details_res.is_successful():
        print(attack_details_res.get_data())
    else:
        print(attack_details_res.get_error_msg())
        return

    if client_choice == AttackType.SYN_FLOOD_DIRECT or client_choice == AttackType.SYN_FLOOD_SPOOFED:
        handle_syn_flood_attack(target_address, target_port, number_of_packets, client_choice)

    elif client_choice == AttackType.URL_BRUTE_FORCE:
        handle_url_brute_force_attack(target_address, target_port, number_of_packets)

    elif client_choice == AttackType.ICMP_SMURF:
        handle_icmp_smurf_attack(target_address, number_of_packets)

    else:
        print("Invalid attack choice. Only 1-3 are allowed.")


def handle_country_request():
    ip_address = input("Enter IP address to check it's country: ")
    client_res = client_controller.send_country_request(ip_address)
    if client_res.is_successful():
        print(client_res.get_data())
    else:
        print(client_res.get_error_msg())


def handle_all_ips_request():
    country = input("Enter country code to receive its addresses: ")
    # todo: add date filtering
    client_res = client_controller.send_get_all_addresses_in_country_request(country)
    if client_res.is_successful():
        print(client_res.get_data())
    else:
        print(client_res.get_error_msg())


def handle_top_countries_request():
    print("Retrieving top countries from the server...")
    client_res = client_controller.send_get_top_countries_request()
    if client_res.is_successful():
        print(client_res.get_data())
    else:
        print(client_res.get_error_msg())


def main():
    print("Hello to GEO-Location Client!")
    client_choice = 0
    while client_choice != GOODBYE_CHOICE:
        print_options_to_client()
        client_choice = int(input())
        if client_choice == 4:
            handle_attack()
        elif client_choice == 1:
            handle_country_request()
        elif client_choice == 2:
            handle_all_ips_request()
        elif client_choice == 3:
            handle_top_countries_request()
        elif client_choice == 5:
            print("Exiting the program, Goodbye!")
        else:
            print("Invalid choice. Only options 1-5 are allowed.")


if __name__ == "__main__":
    main()
