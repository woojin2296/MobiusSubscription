import threading, requests, json, atexit, uuid
import paho.mqtt.client as mqtt

class MobiusSubscription:

    # Constructor to initialize the connection settings for the Mobius server
    def __init__(self, cse_host, cse_port, ae_name, endpoint, cse_mqttport=1883, cse_name="Mobius", origin="UbicompSub"):
        
        # Configuration details for the Mobius CSE (Common Service Entity)
        self.cse_host = cse_host
        self.cse_port = cse_port
        self.cse_mqttport = cse_mqttport
        self.cse_name = cse_name

        # Configuration details for the AE (Application Entity)
        self.ae_name = ae_name

        # The endpoint in Mobius where notifications will be sent (e.g., container name)
        self.endpoint = endpoint

        # Authentication information and request ID for sending requests to the Mobius server
        self.origin = f'{origin}_{endpoint}'
        self.ri = f"UbicompSub_{uuid.uuid4()}"  # Updated to use UUID

        # Base URL for accessing the Mobius server
        self.base_url = f"http://{self.cse_host}:{self.cse_port}/{self.cse_name}/{self.ae_name}/{self.endpoint}"
        
        # Name of the subscription to be created
        self.subscription_name = "UbicompSub"

        # Topic for receiving notifications via MQTT
        self.topic = f"/oneM2M/req/+/{self.origin}/#"

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.__on_connect
        self.client.on_subscribe = self.__on_subscribe
        self.client.on_message = self.__on_message

        atexit.register(self.stop)

    def run(self):
        self.thread = threading.Thread(target=self.__thread)
        self.stop_event = threading.Event()
        self.thread.start()

    def stop(self):
        # Stop the MQTT client loop and disconnect
        self.client.loop_stop()
        self.client.disconnect()
        self.__delete_subscription()
        
        # Signal the thread to exit if necessary
        if self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()
            
        print(f"MobiusSubscription for '{self.base_url}' stopped successfully.")

    def __thread(self):
        if self.__create_subscription():
            self.__setup_mqtt_client()

    def __create_subscription(self):
        # Create a subscription on the Mobius server
        headers = {
            "X-M2M-RI": self.ri,
            "X-M2M-Origin": self.origin,
            "Content-Type": "application/json;ty=23",
            "Accept": "application/json"
        }
        payload = {
            "m2m:sub": {
                "rn": self.subscription_name,
                "nu": [f"mqtt://{self.cse_host}/{self.origin}?ct=json"],
                "nct": 2,
                "enc": {
                    "net": [3]
                }
            }
        }

        try:
            response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))

            if response.status_code == 201:
                print(f"Subscription on '{self.cse_name}/{self.ae_name}/{self.endpoint}' created successfully.")
                return True
            
            elif response.status_code == 404:
                print(f"Endpoint not found: {self.cse_name}/{self.ae_name}/{self.endpoint}")
                return False
            
            else:
                print(f"Failed to create subscription. Status code: {response.status_code}, Response: {response.text}")
                return False
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            return False

    def __delete_subscription(self):
        # Unsubscribe from the Mobius server
        unsubscribe_url = f"{self.base_url}/{self.subscription_name}"
        headers = {
            "X-M2M-RI": self.ri,
            "X-M2M-Origin": self.origin,
        }

        try:
            response = requests.delete(unsubscribe_url, headers=headers)
            if response.status_code == 200 or response.status_code == 204:
                print(f"Unsubscribed '{unsubscribe_url}' successfully.")
            else:
                print(f"Failed to unsubscribe '{unsubscribe_url}'. Status code: {response.status_code}, Response: {response.text}")
        except requests.RequestException as e:
            print(f"HTTP request failed during unsubscribe: {e}")

    def __setup_mqtt_client(self):
        # Set up the MQTT client and start listening for messages
        try:
            self.client.connect(self.cse_host, self.cse_mqttport, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")

    def __on_connect(self, client, userdata, flags, rc, properties=None):
        # Callback function when MQTT client connects to the broker
        if rc == 0:
            print(f"Connected to MQTT broker at {self.cse_host}:{self.cse_mqttport}")

            self.client.subscribe(self.topic)
        else:
            print(f"Connection failed with code {rc}")

    def __on_subscribe(self, client, obj, mid, granted_qos, properties=None):
        # Callback function when subscription is successful
        print(f"Subscription to '{self.topic}' created.")

    def __on_message(self, client, userdata, msg):
        # Callback function when a message is received
        print(f"Message received on topic {msg.topic}")
        try:
            payload = json.loads(msg.payload.decode())
            con_value = payload.get("pc", {}).get("m2m:sgn", {}).get("nev", {}).get("rep", {}).get("m2m:cin", {}).get("con", None)
            subscription_resource = payload.get("pc", {}).get("m2m:sgn", {}).get("sur", None)
        
            if subscription_resource is not None:
                print(f"Subscription Resource (sur): {subscription_resource}")
            else:
                print("Failed to extract 'sur' from the payload.")

            if con_value is not None:
                print(f"Content (con): {con_value}")
            else:
                print("Failed to extract 'con' from the payload.")
            
        except json.JSONDecodeError:
            print("Failed to decode message as JSON")