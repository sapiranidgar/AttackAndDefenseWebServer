import logging
import sqlite3
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

DB_NAME = "geolocation_server"
GEOLOCATION_TABLE_NAME = "geolocation"
COUNTRY_FIELD_NAME = "country"
IP_ADDRESS_FIELD_NAME = "ip_address"
REQUEST_DATE_FIELD_NAME = "request_date"

CREATE_TABLE_COMMAND = f"""CREATE TABLE IF NOT EXISTS {GEOLOCATION_TABLE_NAME} (
    country      TEXT    NOT NULL,
    ip_address   TEXT    NOT NULL,
    request_date NUMERIC NOT NULL
);"""

GET_IP_COUNT_PER_COUNTRY_SORTED_COMMAND = f"""(SELECT {COUNTRY_FIELD_NAME}, COUNT(DISTINCT {IP_ADDRESS_FIELD_NAME}) as ip_count FROM {GEOLOCATION_TABLE_NAME} GROUP BY {COUNTRY_FIELD_NAME} ORDER BY ip_count DESC)"""


class ServerDatabase:
    def __init__(self):
        self.__create_table()

    def __create_cusor(self) -> tuple:
        try:
            db_connection = sqlite3.connect(DB_NAME)
            return db_connection, db_connection.cursor()
        except Exception as e:
            error_msg = f"Failed to connect to database: {DB_NAME}. The error was: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def __commit_and_close_connection(self, server_connection):
        try:
            server_connection.commit()
            server_connection.close()
        except Exception as e:
            error_msg = f"Failed to close the connection to database: {DB_NAME}. The error was: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def __close_connection_and_raise_an_error(self, server_connection, error_msg: str):
        self.__commit_and_close_connection(server_connection)
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    def __create_table(self):
        server_connection, server_cursor = self.__create_cusor()
        try:
            server_cursor.execute(CREATE_TABLE_COMMAND)
        except Exception as e:
            self.__close_connection_and_raise_an_error(server_connection,
                                                       "Failed to create the table. The error was: {}".format(e))

        self.__commit_and_close_connection(server_connection)

    def insert_record(self, country: str, ip_address: str, date: datetime):
        server_connection, server_cursor = self.__create_cusor()
        insert_command = f"INSERT INTO {GEOLOCATION_TABLE_NAME} VALUES (?,?,?)"
        new_record = (country, ip_address, date)

        try:
            server_cursor.execute(insert_command, new_record)
        except Exception as e:
            self.__close_connection_and_raise_an_error(server_connection,
                                                       "Failed to insert the new record. The error was: {}".format(e))

        self.__commit_and_close_connection(server_connection)

    def get_records_by_country(self, country: str, start_date: Optional[datetime], end_date: Optional[datetime]) \
            -> list[str]:
        server_connection, server_cursor = self.__create_cusor()
        select_command = f"""SELECT {IP_ADDRESS_FIELD_NAME} FROM {GEOLOCATION_TABLE_NAME} WHERE {COUNTRY_FIELD_NAME} = '{country}'"""

        if start_date is not None:
            select_command += f" AND {REQUEST_DATE_FIELD_NAME} >= '{start_date}'"
        if end_date is not None:
            select_command += f" AND {REQUEST_DATE_FIELD_NAME} <= '{end_date}'"
        select_command += ";"

        try:
            server_cursor.execute(select_command)
            ip_records = [ip_record[0] for ip_record in server_cursor.fetchall()]
        except Exception as e:
            self.__close_connection_and_raise_an_error(server_connection,
                                                       "Failed to get the records of the country. The error was: {}".format(
                                                           e))
            return []

        self.__commit_and_close_connection(server_connection)
        return ip_records

    def get_countries_with_most_ips(self, number_of_top_countries: int) -> list[str]:
        server_connection, server_cursor = self.__create_cusor()
        select_command = f"""SELECT {COUNTRY_FIELD_NAME} FROM {GET_IP_COUNT_PER_COUNTRY_SORTED_COMMAND} LIMIT {number_of_top_countries};"""

        try:
            server_cursor.execute(select_command)
            country_records = [country_record[0] for country_record in server_cursor.fetchall()]
        except Exception as e:
            self.__close_connection_and_raise_an_error(server_connection,
                                                       "Failed to get the records of top countries. The error was: {}".format(
                                                           e))
            return []

        self.__commit_and_close_connection(server_connection)
        return country_records

    def get_all_countries(self) -> list[str]:
        server_connection, server_cursor = self.__create_cusor()
        select_command = f"""SELECT DISTINCT {COUNTRY_FIELD_NAME} FROM {GEOLOCATION_TABLE_NAME};"""

        try:
            server_cursor.execute(select_command)
            country_records = [country_record[0] for country_record in server_cursor.fetchall()]
        except Exception as e:
            self.__close_connection_and_raise_an_error(server_connection,
                                                       "Failed to get the records of top countries. The error was: {}".format(
                                                           e))
            return []

        self.__commit_and_close_connection(server_connection)
        return country_records
