import json, sqlite3
import paho.mqtt.client as mqtt

db = sqlite3.connect("data.db", check_same_thread=False)
db.execute("PRAGMA journal_mode=WAL")
db.execute("""CREATE TABLE IF NOT EXISTS readings(
    ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    topic TEXT, temp REAL, hum REAL)""")

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe("home/+/climate")

def on_message(client, userdata, msg):
    d = json.loads(msg.payload)
    db.execute("INSERT INTO readings(topic, temp, hum) VALUES (?,?,?)",
               (msg.topic, d["temp"], d["hum"]))
    db.commit()
    print("stored", msg.topic, d)

c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
c.on_connect = on_connect
c.on_message = on_message
c.connect("localhost", 1883)
c.loop_forever()
