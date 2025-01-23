import can
import time
import threading

def initialize_bus(channel="PCAN_USBBUS1", bitrate=500000):
    """Initialize the CAN bus using python-can for PCAN hardware."""
    try:
        bus = can.interface.Bus(channel=channel, bustype='pcan', bitrate=bitrate)
        print("PCAN bus initialized successfully.")
        return bus
    except Exception as e:
        print(f"Error initializing PCAN bus: {e}")
        return None

def send_single_message(bus, message_id, data):
    """Send a single CAN message."""
    try:
        message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
        bus.send(message)
        # print(f"Sent message: ID={hex(message_id)}, Data={data}")
    except Exception as e:
        print(f"Error sending message: {e}")

def send_message_id1(bus, message_id, data, interval):
    """Thread for continuously sending MESSAGE_ID1."""
    while True:
        send_single_message(bus, message_id, data)
        time.sleep(interval)  # Constant interval for MESSAGE_ID1

def send_message_id2(bus, message_id, data, base_interval, sleep_time):
    """Thread for sending MESSAGE_ID2 with periodic delay."""
    i = 0
    count = 1

    while True:
        if i == 50 * count:
            print("Entered delay for MESSAGE_ID2")
            time.sleep(sleep_time * 22)  # Only this thread experiences delay
            print("CAN loss Duration->", sleep_time * count)
            print("count->", count)

            count += 1  # Increment count

            # Reset `i` and `count` when `count == 19`
            if count == 19:
                print("Resetting i and count")
                i = 0
                count = 1
                print("Reset complete. Starting again.")

        send_single_message(bus, message_id, data)
        time.sleep(base_interval)  # Regular interval for MESSAGE_ID2
        i += 1

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"
    BITRATE = 500000
    MESSAGE_ID1 = 0x18530902
    DATA1 = [0x00, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    MESSAGE_ID2 = 0x00000008
    DATA2 = [0x63, 0x00, 0x00, 0x00, 0x00, 0x64, 0x00, 0x00]
    
    BASE_INTERVAL = 0.25  # Regular time interval for sending messages
    SLEEP_TIME = 0.25  # Initial delay for MESSAGE_ID2 when `i == 50 * count`

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)

    if bus:
        # Create separate threads for each message
        thread1 = threading.Thread(target=send_message_id1, args=(bus, MESSAGE_ID1, DATA1, BASE_INTERVAL))
        thread2 = threading.Thread(target=send_message_id2, args=(bus, MESSAGE_ID2, DATA2, BASE_INTERVAL, SLEEP_TIME))

        # Start threads
        thread1.start()
        thread2.start()

        # Keep the main thread alive
        thread1.join()
        thread2.join()

        # Close the bus connection (This will never execute unless the program is stopped)
        bus.shutdown()
