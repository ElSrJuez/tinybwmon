# tinybwmon

A minimal Flask app to monitor and chart your internet bandwidth using speedtest-cli. Stores results in SQLite and supports configurable chart intervals.

## Features
- Runs speed tests (download, upload, ping) using speedtest-cli
- Stores results in a local SQLite database
- Configurable intervals for last hour, 24 hours, 7 days, and month
- Simple API endpoints for running tests and retrieving results
- Automated background speed tests at a configurable cadence
- DHTML web UI for results and status

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Installation
```powershell
# Clone the repository
cd tinybwmon
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage
```powershell
python main.py
```
Visit [http://127.0.0.1:42042/](http://127.0.0.1:42042/) in your browser.

### Endpoints
- `/` — Home/info and status dashboard
- `/run_test` — Run a speed test and store the result
- `/results/<interval>` — Get results for a given interval (`last_hour`, `last_24_hours`, `last_7_days`, `last_month`)
- `/view/<interval>` — DHTML chart for a given interval

## Configuration
Edit `config.ini` to change interval durations for charting, or set environment variables (e.g., `LAST_HOUR`).

To configure the background speed test cadence, set `test_interval_minutes` in the `[scheduler]` section of `config.ini` or use the `TEST_INTERVAL_MINUTES` environment variable.

## Data Retention and Storage
**Note:** The current implementation uses a round-robin/circular buffer for data storage, ensuring the database does not grow indefinitely.

## Roadmap
- [x] Configurable chart intervals and test cadence
- [x] Automated background speed tests
- [x] REST API for results and manual test trigger
- [x] Basic web UI for charting results and status
- [x] Round-robin storage logic
- [ ] Docker support for easy deployment
- [ ] Logging and error reporting improvements
- [ ] Optional authentication/rate limiting for endpoints
- [ ] **True round-robin/circular buffer storage** (future improvement)

## Contributing
Contributions are welcome! Please open issues or pull requests for bug fixes, features, or suggestions. See [CONTRIBUTING.md](CONTRIBUTING.md) if available.

## License
MIT
