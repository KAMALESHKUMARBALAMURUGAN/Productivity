import can
import time

def initialize_bus(channel="PCAN_USBBUS1", bitrate=500000):
    """
    Initialize the CAN bus using python-can for PCAN hardware.
    """
    try:
        # Initialize the PCAN interface
        bus = can.interface.Bus(channel=channel, bustype='pcan', bitrate=bitrate)
        print("PCAN bus initialized successfully.")
        return bus
    except Exception as e:
        print(f"Error initializing PCAN bus: {e}")
        return None

def send_same_message_n_times(bus, message_id, interval_ms, data, n):
    """Send the same CAN message n times over the CAN bus."""
    try:
        for _ in range(n):
            print("The No of message sent: ",_)
            # Create a CAN message
            message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
            # Send the message
            bus.send(message)
            print(f"Sent message: ID={hex(message_id)}, Data={data}")
            # Wait for the specified interval
            time.sleep(interval_ms / 1000.0)
    except Exception as e:
        print(f"Error sending messages: {e}")

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"  # Replace with your actual PCAN channel
    BITRATE = 500000          # CAN bitrate
    MESSAGE_ID = 0x14520902   # Example CAN message ID
    INTERVAL_MS = 250         # Message interval in milliseconds
    N = 240                    # Number of times to send the message

    # Example data to send
    data = [0x8D, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] #SPEED - 60
    # data = [0xF1, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] #SPEED - 45
    # data = [0x47, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] #SPEED - 30

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)

    if bus:
        # Send the same message n times
        send_same_message_n_times(bus, MESSAGE_ID, INTERVAL_MS, data, N)
        # Close the bus connection
        bus.shutdown()