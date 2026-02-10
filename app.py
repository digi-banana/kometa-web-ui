import os, subprocess, threading, shutil, docker, yaml, difflib
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
scheduler = APScheduler()
docker_client = docker.from_env()

# Paths
CONFIG_DIR = "/app/kometa_config"
BACKUP_DIR = "/app/config_backups"
LOG_DIR = "/app/logs"
ASSET_DIR = os.path.join(CONFIG_DIR, "assets")

for d in [BACKUP_DIR, LOG_DIR, ASSET_DIR]:
    os.makedirs(d, exist_ok=True)

def run_kometa_sync(dry_run=False):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"run_{timestamp}.log")
    
    try:
        container = docker_client.containers.get("kometa")
        cmd = "python kometa.py --run"
        if dry_run: cmd += " --tests"
        
        exec_log = container.exec_run(cmd, stream=True)
        with open(log_file, "w") as f:
            for line in exec_log.output:
                clean_line = line.decode('utf-8').strip()
                f.write(clean_line + "\n")
                socketio.emit('log_update', {'data': clean_line})
    except Exception as e:
        socketio.emit('log_update', {'data': f"Error: {str(e)}"})

@app.route('/')
def index(): return render_template('index.html')

@app.route('/list_configs')
def list_configs():
    files = [f for f in os.listdir(CONFIG_DIR) if f.endswith(('.yml', '.yaml'))]
    return jsonify({"files": files})

@app.route('/get_config/<filename>')
def get_config(filename):
    with open(os.path.join(CONFIG_DIR, filename), 'r') as f:
        return jsonify({"content": f.read()})

@app.route('/save_config', methods=['POST'])
def save_config():
    data = request.json
    filename, content = data['filename'], data['content']
    try:
        yaml.safe_load(content) # Validation
        # Backup existing
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(os.path.join(CONFIG_DIR, filename), os.path.join(BACKUP_DIR, f"{filename}_{ts}.bak"))
        with open(os.path.join(CONFIG_DIR, filename), 'w') as f:
            f.write(content)
        return jsonify({"status": "success", "message": "Saved & Backed up"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/upload_poster', methods=['POST'])
def upload_poster():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(ASSET_DIR, filename))
    return jsonify({"status": "success", "url": f"/assets/{filename}"})

@app.route('/assets/<filename>')
def serve_asset(filename):
    return send_from_directory(ASSET_DIR, filename)

@app.route('/set_schedule', methods=['POST'])
def set_schedule():
    cron = request.json.get("cron").split()
    scheduler.add_job(id='sync', func=run_kometa_sync, trigger='cron', 
                      minute=cron[0], hour=cron[1], day=cron[2], month=cron[3], day_of_week=cron[4])
    return jsonify({"message": "Schedule set"})

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    socketio.run(app, host='0.0.0.0', port=8461)
