# Python Program for Multi-threaded Subscriptions to Mobius Resources

This project provides a Python program that subscribes to Mobius platform resources and reads the `con` (content) of the `cin` (content instances) created in those resources. Each subscription operates on a separate thread to prevent any interference or conflicts, supporting multiple concurrent subscriptions.

## Key Features

- **Subscription Creation:** Creates subscriptions to specific Application Entities (AEs) and containers (endpoints) on the Mobius server.
- **MQTT Client Setup:** Uses the MQTT protocol to communicate with the Mobius server and receive notifications.
- **Message Handling:** Processes incoming MQTT messages to extract and display the `con` value of the `cin`.
- **Multi-threaded Subscription Management:** Each subscription runs on a separate thread, allowing for independent operation.
- **Unsubscription and Resource Cleanup:** Safely unsubscribes and closes connections when the program exits.

## Getting Started

### Prerequisites

- **Python 3.x** installed on your system.
- Install the required libraries:

  ```bash
  pip install paho-mqtt requests
  ```

### Code Download

Clone this repository or download the necessary files:

```bash
git clone https://github.com/yourusername/mobius-subscription.git
```

## Usage

### Import the `MobiusSubscription` Class

```python
from mobius_subscription import MobiusSubscription
```

### Create and Run Subscription Instances Exemple

```python
# Create the first subscription instance
subscription1 = MobiusSubscription(
    cse_host="YOUR_MOBIUS_HOST",
    cse_port=YOUR_MOBIUS_PORT,
    ae_name="YOUR_AE_NAME",
    endpoint="YOUR_CONTAINER_NAME_1"
)
subscription1.run()

# Create the second subscription instance
subscription2 = MobiusSubscription(
    cse_host="YOUR_MOBIUS_HOST",
    cse_port=YOUR_MOBIUS_PORT,
    ae_name="YOUR_AE_NAME",
    endpoint="YOUR_CONTAINER_NAME_2"
)
subscription2.run()
```

### Maintain Program Execution and Handle Exit

```python
try:
    while True:
        # The main thread can perform other tasks or remain idle
        pass
except KeyboardInterrupt:
    # On program exit, unsubscribe and clean up resources
    subscription1.stop()
    subscription2.stop()
```

## Class Details

### `MobiusSubscription` Class Initialization

```python
MobiusSubscription(
    cse_host,           # Host address of the Mobius server (e.g., "203.253.128.177")
    cse_port,           # Port number of the Mobius server (e.g., 7579)
    ae_name,            # Name of the AE to subscribe to (e.g., "SubTest")
    endpoint,           # Name of the container to subscribe to (e.g., "testcnt1")
    cse_mqttport=1883,  # (Optional) MQTT port number, default is 1883
    cse_name="Mobius",  # (Optional) Name of the CSE, default is "Mobius"
    origin="UbicompSub" # (Optional) Originator identifier, default is "UbicompSub"
)
```

- **cse_host:** IP address or domain name of the Mobius server.
- **cse_port:** HTTP port number of the Mobius server.
- **ae_name:** Name of the AE where the subscription will be created.
- **endpoint:** Name of the container to subscribe to.
- **cse_mqttport:** (Optional) Port number of the MQTT broker. Default is 1883.
- **cse_name:** (Optional) Name of the Mobius CSE. Default is "Mobius".
- **origin:** (Optional) Originator identifier. Default is "UbicompSub".

### Main Methods

- **run():** Creates the subscription and sets up the MQTT client to start receiving messages.
- **stop():** Unsubscribes from the Mobius server and stops the MQTT connection and thread.

## Execution Flow

1. **Instance Creation:** Instantiate the `MobiusSubscription` class with the required parameters.
2. **Start Subscription:** Call the `run()` method to create the subscription and start the MQTT client.
3. **Receive and Handle Messages:** Each subscription operates on a separate thread, receiving messages independently. When a new `cin` is created, it outputs the `con` value.
4. **Program Termination and Resource Cleanup:** When the program ends or subscriptions are no longer needed, call the `stop()` method to unsubscribe and clean up resources.

## Notes

- **Mobius Server Configuration:** Ensure that `cse_host`, `cse_port`, `ae_name`, and `endpoint` are set according to your actual environment.
- **Pre-existing AE and Containers:** The AE and containers (endpoints) you wish to subscribe to must already exist on the Mobius server.
- **Resource Cleanup:** Always call the `stop()` method when the program exits to safely unsubscribe and close connections.
- **Exception Handling:** Use a `try-except` block to handle unexpected terminations and ensure resources are properly released.

## License

This project is distributed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests.

## Contact

For questions or inquiries, please contact [woojin2296@kakao.com](mailto:woojin2296@kakao.com).
