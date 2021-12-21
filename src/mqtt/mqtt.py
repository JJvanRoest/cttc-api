from config import CONFIG

from paho.mqtt import client as mqtt_client


class Worker:
    def __init__(self):
        _config = CONFIG.mqtt
        self.client_id = _config["client"]
        self.broker = _config["broker"]
        self.port = _config["port"]
        self.topic = _config["topic"]
        self.client = self.connect_mqtt()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker.")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id=self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client
