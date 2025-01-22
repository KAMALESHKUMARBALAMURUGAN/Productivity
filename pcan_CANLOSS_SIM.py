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

def send_single_message(bus, message_id, byte_value):
    """Send a single CAN message with the specified ID and byte value."""
    try:
        # Create a CAN message with the specified byte value at the last position
        data = [0x00, byte_value, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
        # Send the message
        bus.send(message)
        # print(f"Sent message: ID={hex(message_id)}, Data={data}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"  # Replace with your actual PCAN channel
    BITRATE = 500000          # CAN bitrate
    MESSAGE_ID = 0x18530902   # New CAN message ID
    BYTE_VALUE = 0x24         # Byte value to be set at the last position
    N=10

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)

    if bus:
           # Send the single message N times
        for i in range(N):
            print("Number of messages sent",i+1)
            send_single_message(bus, MESSAGE_ID, BYTE_VALUE)
            if i == 4:  # Add a 250 ms break after the 5th message
                time.sleep(2.00)
            else:
             time.sleep(0.1)  # Optional: Add a delay between messages
        # Close the bus connection
        bus.shutdown()