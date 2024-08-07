from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)

SESSION_FILE = "session.txt"
NEWS_FILE = "news.txt"
VERSION_FILE = "version.txt"
SESSION_TIMEOUT = 600  # 10 минут

def read_sessions():
    if not os.path.exists(SESSION_FILE):
        return []
    
    with open(SESSION_FILE, 'r') as file:
        return file.readlines()

def write_sessions(sessions):
    with open(SESSION_FILE, 'w') as file:
        file.writelines(sessions)

def update_sessions(session_id):
    current_time = int(time.time())
    last_time = current_time - SESSION_TIMEOUT

    sessions = read_sessions()
    updated_sessions = []
    session_found = False

    for session in sessions:
        sid, timestamp = session.strip().split("|")
        timestamp = int(timestamp)

        if timestamp > last_time:
            if sid == session_id:
                timestamp = current_time
                session_found = True
            updated_sessions.append(f"{sid}|{timestamp}\n")

    if not session_found:
        updated_sessions.append(f"{session_id}|{current_time}\n")

    write_sessions(updated_sessions)

def count_online_users():
    current_time = int(time.time())
    last_time = current_time - SESSION_TIMEOUT

    sessions = read_sessions()
    online_users = [session for session in sessions if int(session.strip().split("|")[1]) > last_time]
    return len(online_users)

def read_news():
    if not os.path.exists(NEWS_FILE):
        return "No news available."
    
    with open(NEWS_FILE, 'r') as file:
        return file.read()

def read_version():
    if not os.path.exists(VERSION_FILE):
        return "0"
    
    with open(VERSION_FILE, 'r') as file:
        return file.read().strip()

@app.route('/')
def index():
    session_id = request.args.get('session_id')
    online_users_count = count_online_users()
    if session_id:
        update_sessions(session_id)
    return str(online_users_count), 200

@app.route('/online')
def online():
    online_users_count = count_online_users()
    return str(online_users_count), 200

@app.route('/news')
def news():
    news_content = read_news()
    return news_content, 200

@app.route('/version')
def version():
    version_content = read_version()
    return version_content, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7771)
