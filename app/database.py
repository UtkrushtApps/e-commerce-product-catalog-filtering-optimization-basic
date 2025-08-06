import psycopg2
import psycopg2.extras

def get_connection():
    conn = psycopg2.connect(
        dbname='ecommerce_db',
        user='fastapi_user',
        password='fastapi_pass',
        host='postgres',
        port=5432
    )
    return conn