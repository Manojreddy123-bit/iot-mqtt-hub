# MQTT IoT Sensor Hub (Raspberry Pi 5)

An end-to-end IoT monitoring system: a sensor node publishes readings over MQTT, a logger stores them in SQLite, and a Flask dashboard shows live values and trends.

## Architecture

```
node_sim.py (ESP32 planned)
        |  MQTT: home/node1/climate
        v
   Mosquitto broker
        |  subscribe: home/+/climate
        v
    logger.py  -->  SQLite (data.db)  -->  Flask API + Chart.js dashboard
```

## Components

| File | Purpose |
|---|---|
| `node_sim.py` | Simulated sensor node publishing temperature and humidity every 5 s |
| `logger.py` | MQTT subscriber that stores readings in SQLite |
| `app.py` | Flask app serving a JSON API and a live Chart.js dashboard |
| `systemd/` | Service files so everything starts on boot |

## Tech stack

Raspberry Pi 5, Raspberry Pi OS, Mosquitto, Python (paho-mqtt, Flask), SQLite, Chart.js, systemd

## Setup

1. Install the broker and tools:
   `sudo apt install -y mosquitto mosquitto-clients sqlite3 python3-venv`
2. Add `/etc/mosquitto/conf.d/local.conf` with:
   `listener 1883` and `allow_anonymous true` (home network only)
3. Create the environment:
   `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
4. Copy the files in `systemd/` to `/etc/systemd/system/`, edit the user and paths, then run:
   `sudo systemctl daemon-reload && sudo systemctl enable --now iot-logger iot-sim iot-dashboard`
5. Open `http://<pi-ip>:5000` on a device on the same network.

## Screenshots

![Dashboard](docs/dashboard.png)

## Roadmap

- Replace the simulator with an ESP32 + DHT22/BME280 node
- Telegram alerts on threshold
- Relay control from the dashboard
- MQTT authentication and TLS
