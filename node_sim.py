import json, time, random
import paho.mqtt.client as mqtt

c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
c.connect("localhost", 1883)
c.loop_start()

while True:
    data = {"temp": round(random.uniform(24, 34), 1),
            "hum": round(random.uniform(40, 70), 1)}
    c.publish("home/node1/climate", json.dumps(data))
    print("sent", data)
    time.sleep(5)
