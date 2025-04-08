import psycopg2

try:
    conn = psycopg2.connect(
        dbname="<your_db>",
        user="<user-name>",
        password="<password>",
        host="<azure-host>.postgres.database.azure.com",
        port="5432",
        sslmode="require"
    )
    print("Connected successfully to Azure PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
