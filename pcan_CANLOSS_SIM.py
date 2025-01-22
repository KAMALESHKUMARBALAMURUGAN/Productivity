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

def send_single_message(bus, message_id, data):
    """Send a single CAN message with the specified ID and data."""
    try:
        message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
        # Send the message
        bus.send(message)
        print(f"Sent message: ID={hex(message_id)}, Data={data}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"  # Replace with your actual PCAN channel
    BITRATE = 500000          # CAN bitrate
    MESSAGE_ID1 = 0x18530902  # First CAN message ID
    DATA1 = [0x00, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Data for first message
    MESSAGE_ID2 = 0x00000008  # Second CAN message ID
    DATA2 = [0x63, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Data for second message
    N = 10                    # Number of times to send the messages

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)

    if bus:
        # Send the messages N times
        for i in range(N):
            print("Number of messages sent", i + 1)
            send_single_message(bus, MESSAGE_ID1, DATA1)
            send_single_message(bus, MESSAGE_ID2, DATA2)
            if i == 4:  # Add a 250 ms break after the 5th message
                time.sleep(2.00)
            else:
                time.sleep(0.1)  # Optional: Add a delay between messages

        # Close the bus connection
        bus.shutdown()