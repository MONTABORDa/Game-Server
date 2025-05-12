from flask import Flask, request
import subprocess
from log_stats import log_server_stat

app = Flask(__name__)

def run_script(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Erreur: {e.output}"

@app.route("/activate", methods=["POST"])
def activate():
    data = request.json
    map_name = data.get("map")
    map_type = data.get("type")
    return run_script(f"./scripts/activate-map.sh {map_name} {map_type}")

@app.route("/deactivate", methods=["POST"])
def deactivate():
    data = request.json
    map_name = data.get("map")
    map_type = data.get("type")
    return run_script(f"./scripts/deactivate-map.sh {map_name} {map_type}")

@app.route("/backup", methods=["POST"])
def backup():
    return run_script("./scripts/backup.sh")

@app.route("/rotate", methods=["POST"])
def rotate():
    return run_script("./scripts/rotate-backups.sh")

@app.route("/reboot", methods=["POST"])
def reboot():
    return run_script("./scripts/daily-reboot.sh")

@app.route("/logstat", methods=["POST"])
def logstat():
    data = request.json
    map_name = data.get("map_name")
    player_count = data.get("player_count", 0)
    status = data.get("status", "unknown")
    return log_server_stat(map_name, player_count, status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


@app.route("/stats", methods=["GET"])
def get_stats():
    import psycopg2
    import json
    try:
        conn = psycopg2.connect(
            dbname='gamestats',
            user='admin',
            password='changeme',
            host='db'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, map_name, player_count, status FROM server_stats ORDER BY timestamp DESC LIMIT 100")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        result = []
        for row in rows:
            result.append({
                'timestamp': row[0].isoformat(),
                'map_name': row[1],
                'player_count': row[2],
                'status': row[3]
            })
        return json.dumps(result), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return f"Erreur lors de la récupération des stats : {e}", 500


@app.route("/exportstats", methods=["POST"])
def export_stats():
    return run_script("./scripts/export-stats.sh")
