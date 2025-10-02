from fastapi import FastAPI
import pyodbc
import os
from azure.identity import DefaultAzureCredential

app = FastAPI()

@app.get("/dbcheck")
def check_db():
    try:
        # Get server & DB name from environment variables
        server = os.getenv("DB_SERVER")   # e.g. "sample-server-app-service.database.windows.net"
        database = os.getenv("DB_NAME")   # e.g. "sample_db"

        if not server or not database:
            return {"status": "error", "message": "DB_SERVER or DB_NAME env var not set"}

        # Get access token from Managed Identity
        credential = DefaultAzureCredential()
        token = credential.get_token("https://database.windows.net/.default")

        # Build connection string
        conn_str = (
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server={server};"
            f"Database={database};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )

        # Connect with token
        conn = pyodbc.connect(conn_str, attrs_before={1256: token.token})
        cursor = conn.cursor()

        # Simple test query
        cursor.execute("SELECT DB_NAME();")
        row = cursor.fetchone()

        return {"status": "connected", "database": row[0]}

    except Exception as e:
        return {"status": "not connected", "error": str(e)}
