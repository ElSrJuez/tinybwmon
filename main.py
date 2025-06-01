# this is an enxtremely basic flask app that uses the speedtest-cli library to get, store and chart internet upload/download speeds
# it uses sqllight but in a round-robin style to chart the last 7 days, last 24 hours and last hour with configurable intervals

import os
import configparser
from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
from datetime import datetime, timedelta
import speedtest
import threading
import time

# Load intervals from config file or environment variables
config = configparser.ConfigParser()
config.read('config.ini')

def get_interval(name, default):
    env_val = os.getenv(name.upper())
    if env_val is not None:
        try:
            return int(env_val)
        except ValueError:
            pass
    if config.has_option('intervals', name):
        try:
            return int(config.get('intervals', name))
        except ValueError:
            pass
    return default

LAST_HOUR = get_interval('last_hour', 60)
LAST_24_HOURS = get_interval('last_24_hours', 24 * 60)
LAST_7_DAYS = get_interval('last_7_days', 7 * 24 * 60)
LAST_MONTH = get_interval('last_month', 30 * 24 * 60)

INTERVALS = {
    'last_hour': LAST_HOUR,
    'last_24_hours': LAST_24_HOURS,
    'last_7_days': LAST_7_DAYS,
    'last_month': LAST_MONTH
}

app = Flask(__name__)
DB_PATH = 'data/speedtest_results.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            download REAL,
            upload REAL,
            ping REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def insert_result(download, upload, ping):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Insert the new result
    c.execute('INSERT INTO results (timestamp, download, upload, ping) VALUES (?, ?, ?, ?)',
              (datetime.now(), download, upload, ping))
    conn.commit()

    # Implement round-robin logic for each interval
    for interval_name, minutes in INTERVALS.items():
        since = datetime.now() - timedelta(minutes=minutes)
        c.execute('DELETE FROM results WHERE timestamp < ?', (since,))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html', intervals=INTERVALS)

@app.route('/run_test')
def run_test():
    # Run actual speedtest-cli logic
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # Convert to Mbps
        upload = st.upload() / 1_000_000    # Convert to Mbps
        ping = st.results.ping
        insert_result(download, upload, ping)
        return jsonify({'status': 'ok', 'download': round(download, 2), 'upload': round(upload, 2), 'ping': round(ping, 2)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/results/<interval>')
def get_results(interval):
    if interval not in INTERVALS:
        return jsonify({'error': 'Invalid interval'}), 400
    minutes = INTERVALS[interval]
    since = datetime.now() - timedelta(minutes=minutes)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT timestamp, download, upload, ping FROM results WHERE timestamp >= ? ORDER BY timestamp ASC', (since,))
    rows = c.fetchall()
    conn.close()
    results = [
        {'timestamp': row[0], 'download': row[1], 'upload': row[2], 'ping': row[3]}
        for row in rows
    ]
    return jsonify(results)

@app.route('/view/<interval>')
def view_results(interval):
    if interval not in INTERVALS:
        return f"<h2>Invalid interval: {interval}</h2>", 400
    return render_template('results.html', interval=interval)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

def get_scheduler_interval():
    env_val = os.getenv('TEST_INTERVAL_MINUTES')
    if env_val is not None:
        try:
            return int(env_val)
        except ValueError:
            pass
    if config.has_option('scheduler', 'test_interval_minutes'):
        try:
            return int(config.get('scheduler', 'test_interval_minutes'))
        except ValueError:
            pass
    return 1  # default to 1 minute

SCHEDULER_INTERVAL_MINUTES = get_scheduler_interval()

def scheduled_speedtest():
    while True:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000  # Mbps
            upload = st.upload() / 1_000_000    # Mbps
            ping = st.results.ping
            insert_result(download, upload, ping)
        except Exception as e:
            print(f"Scheduled speedtest error: {e}")
        time.sleep(60 * SCHEDULER_INTERVAL_MINUTES)  # Run every 15 minutes

# Start the background thread when the app starts
threading.Thread(target=scheduled_speedtest, daemon=True).start()
