import psycopg2
from datetime import datetime

def log_server_stat(map_name, player_count, status):
    try:
        conn = psycopg2.connect(
            dbname='gamestats',
            user='admin',
            password='changeme',
            host='db'
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS server_stats (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                map_name TEXT NOT NULL,
                player_count INTEGER,
                status TEXT
            )
        """)
        cursor.execute(
            "INSERT INTO server_stats (timestamp, map_name, player_count, status) VALUES (%s, %s, %s, %s)",
            (datetime.utcnow(), map_name, player_count, status)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return "✅ Stat enregistrée"
    except Exception as e:
        return f"❌ Erreur : {e}"
