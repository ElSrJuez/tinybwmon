# tinybwmon

A minimal Flask app to monitor and chart your internet bandwidth using speedtest-cli. Stores results in SQLite and supports configurable chart intervals.

## Features
- Runs speed tests (download, upload, ping) using speedtest-cli
- Stores results in a local SQLite database
- Configurable intervals for last hour, 24 hours, 7 days, and month
- Simple API endpoints for running tests and retrieving results

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Installation
```powershell
# Clone the repository
# (if you haven't already)
cd tinybwmon
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage
```powershell
python main.py
```
Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

### Endpoints
- `/` — Home/info
- `/run_test` — Run a speed test and store the result
- `/results/<interval>` — Get results for a given interval (`last_hour`, `last_24_hours`, `last_7_days`, `last_month`)

## Configuration
Edit `config.ini` to change interval durations, or set environment variables (e.g., `LAST_HOUR`).

## License
MIT
