# shared/db.py

import os
import pymysql

def get_connection():
    """
    Returns a pymysql.Connection object using environment variables.
    Environment variables (in local.settings.json):
      - MYSQL_HOST
      - MYSQL_PORT
      - MYSQL_USER
      - MYSQL_PASSWORD
      - MYSQL_DATABASE
    """
    host     = os.getenv("MYSQL_HOST", "localhost")
    port     = int(os.getenv("MYSQL_PORT", 3306))
    user     = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "root")
    database = os.getenv("MYSQL_DATABASE", "InvoiceDB")

    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
