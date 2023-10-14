import paho.mqtt.client as mqtt
import json
import ssl
import os

IP_address = "192.168.178.239"
accesscode = "59fe1229"
topic = f"device/#"

key_suffixes = {
    "bed_temper": "°C",
    "nozzle_temper": "°C",
    "nozzle_target_temper": "°C",
    "bed_target_temper": "°C",
    "heatbreak_fan_speed": "%",
    "chamber_temper": "°C",
    "cooling_fan_speed": "%",
    "mc_percent": "%",
    "mc_remaining_time": "min",
    "subtask_name": "",
    "layer_num":""
}

def on_connect(client, userdata, flags, rc):
    if not os.path.exists("overlays"):
        os.makedirs("overlays")
    print(f"Connected: {str(rc)}")
    client.subscribe(topic)

def on_message(client, userdata, msg):

    try:
        payload = json.loads(msg.payload)
        if "print" in payload:
            print_content = payload["print"]
            print(print_content)
            for key, suffix in key_suffixes.items():
                if key in print_content:
                    value_with_suffix = str(print_content[key]) + suffix
                    with open(
                        os.path.join("overlays", f"{key}.txt"), "w", encoding="utf-8"
                    ) as f:
                        f.write(value_with_suffix + "\n")

    except json.JSONDecodeError:
        print("Fehler beim Parsen des JSON.")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("bblp", password=accesscode)
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.connect(IP_address, 8883, 60)
client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
