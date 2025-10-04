import sqlite3
from datetime import datetime
from typing import Optional

DB_NAME = "geolocation_server"
GEOLOCATION_TABLE_NAME = "geolocation"

CREATE_TABLE_COMMAND = f"""CREATE TABLE IF NOT EXISTS {GEOLOCATION_TABLE_NAME} (
    country      TEXT    NOT NULL,
    ip_address   TEXT    NOT NULL,
    request_date NUMERIC NOT NULL
);"""

GET_IP_COUNT_PER_COUNTRY_SORTED_COMMAND = f"""(SELECT country, COUNT(DISTINCT ip_address) as ip_count FROM {GEOLOCATION_TABLE_NAME} GROUP BY country ORDER BY ip_count DESC)"""


class ServerDatabase:
    def __init__(self):
        self.__create_table()

    def __create_cusor(self) -> tuple:
        try:
            db_connection = sqlite3.connect(DB_NAME)
            return db_connection, db_connection.cursor()
        except Exception as e:
            raise "Failed to connect to database. The error was: {}".format(e)

    def __commit_and_close_connection(self, server_connection):
        try:
            server_connection.commit()
            server_connection.close()
        except Exception as e:
            raise "Failed to commit and close the connection. The error was: {}".format(e)

    def __create_table(self):
        server_connection, server_cursor = self.__create_cusor()
        try:
            server_cursor.execute(CREATE_TABLE_COMMAND)
        except Exception as e:
            self.__commit_and_close_connection(server_connection)
            raise "Failed to create the table. The error was: {}".format(e)
        self.__commit_and_close_connection(server_connection)

    def insert_record(self, country: str, ip_address: str, date: datetime):
        server_connection, server_cursor = self.__create_cusor()
        insert_command = f"INSERT INTO {GEOLOCATION_TABLE_NAME} VALUES (?,?,?)"
        new_record = (country, ip_address, date)

        try:
            server_cursor.execute(insert_command, new_record)
        except Exception as e:
            self.__commit_and_close_connection(server_connection)
            raise "Failed to insert the new record. The error was: {}".format(e)
        self.__commit_and_close_connection(server_connection)

    def get_records_by_country(self, country: str, start_date: Optional[datetime], end_date: Optional[datetime]) \
            -> list[str]:
        server_connection, server_cursor = self.__create_cusor()
        select_command = f"""SELECT ip_address FROM {GEOLOCATION_TABLE_NAME} WHERE country = '{country}'"""

        if start_date is not None:
            select_command += f" AND request_date >= '{start_date}'"
        if end_date is not None:
            select_command += f" AND request_date <= '{end_date}'"
        select_command += ";"

        try:
            server_cursor.execute(select_command)
            ip_records = [ip_record[0] for ip_record in server_cursor.fetchall()]
        except Exception as e:
            self.__commit_and_close_connection(server_connection)
            raise "Failed to get the records of the country. The error was: {}".format(e)
        self.__commit_and_close_connection(server_connection)
        return ip_records

    def get_countries_with_most_ips(self, number_of_top_countries: int) -> list[str]:
        server_connection, server_cursor = self.__create_cusor()
        select_command = f"""SELECT country FROM {GET_IP_COUNT_PER_COUNTRY_SORTED_COMMAND} LIMIT {number_of_top_countries};"""

        try:
            server_cursor.execute(select_command)
            country_records = [country_record[0] for country_record in server_cursor.fetchall()]
        except Exception as e:
            self.__commit_and_close_connection(server_connection)
            raise "Failed to get the records of top countries. The error was: {}".format(e)

        self.__commit_and_close_connection(server_connection)
        return country_records
