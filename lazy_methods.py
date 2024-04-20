#!/usr/bin/python3

"""This module defines useful short methods that are heavily used during
testing."""

from os import getenv
from io import StringIO
from uuid import UUID as uuid
from random import choice
import MySQLdb


class LazyMethods:
    """Defines useful short methods that are heavily used during testing."""

    __random_attributes = {
        "first_name": ["John", "Lucy", "Lisa", "Bob", "Betty"],
        "last_name": ["Doe", "Sickle", "Walters", "Range", "Holberton"],
        "age": [45, 98, 23, 40, 12, 67],
        "latitude": [
            37.773972,
            -89.2312,
            -14.5512,
            36.2148,
            45.1231,
            -66.2312,
            78.5512,
        ],
        "longitude": [
            -179.2312,
            -14.5512,
            36.2148,
            145.1231,
            -66.2312,
            78.5512,
        ],
    }

    @staticmethod
    def get_uuid(line: StringIO) -> uuid:
        """Returns the UUID from a string."""
        return uuid(line.getvalue().strip())

    @staticmethod
    def get_instances_count(line: StringIO) -> int:
        """Returns the integer value for the number of instances of a model."""
        return int(line.getvalue().strip())

    @staticmethod
    def get_key(model_name: str, instance_id: uuid) -> str:
        """Generates the key used in the objects dictionary for an instance."""
        return f"{model_name}.{instance_id}"

    def get_first_name(self) -> str:
        """Returns a first name."""
        return choice(self.__random_attributes["first_name"])

    def get_last_name(self) -> str:
        """Returns a first name."""
        return choice(self.__random_attributes["last_name"])

    def get_email(self, first_name: str = None, last_name: str = None) -> str:
        """Returns an email address based on random first and last names."""
        return (
            f"{first_name or self.get_first_name()}."
            f"{last_name or self.get_last_name()}@lzcorp.it".lower()
        )

    def get_random_attribute(self):
        """Generates a random key and a value corresponding to that key."""
        key = choice(list(self.__random_attributes.keys()))

        return key, choice(self.__random_attributes[key])

    @staticmethod
    def set_default_collation(charset="utf8mb4", collate="utf8mb4_unicode_ci"):
        """
        Sets the default collation for the MySQL database and all its tables.

        Args:
            charset (str, optional): The character set to be used. Defaults to
            "utf8mb4".
            collate (str, optional): The collation to be used. Defaults to
            "utf8mb4_unicode_ci".

        This method establishes a connection to the MySQL database, retrieves
        all table names, and sets the default collation for the database and
        each table to the specified charset and collate values. It also
        temporarily disables foreign key checks during the process.

        Note:
            This method requires the following environment variables to be set:
            - HBNB_MYSQL_DB: The name of the MySQL database
            - HBNB_MYSQL_USER: The username for the MySQL database
            - HBNB_MYSQL_PWD: The password for the MySQL database
            - HBNB_MYSQL_HOST: The host address for the MySQL database
        """
        # Establish a database connection
        db = MySQLdb.connect(
            db=f"{getenv('HBNB_MYSQL_DB')}",
            user=f"{getenv('HBNB_MYSQL_USER')}",
            password=f"{getenv('HBNB_MYSQL_PWD')}",
            host=f"{getenv('HBNB_MYSQL_HOST')}",
        )

        # Create a cursor object
        cursor = db.cursor()

        # Execute SQL command to get all table names
        cursor.execute("SHOW TABLES")

        # Fetch all the rows
        tables = cursor.fetchall()

        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        cursor.execute(
            f"ALTER DATABASE {getenv('HBNB_MYSQL_DB')} "
            f"CHARACTER SET = {charset} COLLATE = {collate};"
        )

        for table_name in tables:
            # Execute SQL command to alter table character set
            table_name = table_name[0]

            try:
                cursor.execute(
                    f"ALTER TABLE {table_name} "
                    f"CONVERT TO CHARACTER SET {charset} COLLATE {collate}"
                )
            except MySQLdb.ProgrammingError:
                pass

        cursor.execute("SET FOREIGN_KEY_CHECKS=1")

        # Commit your changes in the database
        db.commit()

        # Disconnect from server
        db.close()
