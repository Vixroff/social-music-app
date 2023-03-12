import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()


with mysql.connector.connect(
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    host = os.getenv('DB_HOST'),
    port = os.getenv('DB_PORT')
) as connection:
    print(f"DB_PORT value: {os.getenv('DB_PORT')}")
    with connection.cursor() as cursor:
        db_name = os.getenv('DB_NAME')
        query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        cursor.execute(query)
        connection.commit()
