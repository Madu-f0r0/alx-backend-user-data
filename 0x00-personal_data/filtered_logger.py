#!/usr/bin/env python3
"""Contains the definition for the function `filter_datum`"""

import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns an obfuscated log message"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    streamHandler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connection to a database and returns the connector"""
    db = mysql.connector.connection.MySQLConnection(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db


def main():
    """Retrieves all rows in the users table and displays them
    under a filtered format
    """
    db = get_db()
    dbCursor = db.cursor()
    dbCursor.execute('SELECT * FROM users;')
    fields = dbCursor.column_names
    logger = get_logger()

    for row in dbCursor:
        message = ''.join('{}={}; '.format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())

    dbCursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor for the RedactingFormatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using `filter_datum`"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
