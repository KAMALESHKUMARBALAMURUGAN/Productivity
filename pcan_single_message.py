import can

def initialize_bus(channel="PCAN_USBBUS1", bitrate=500000):
    """
    Initialize the CAN bus using python-can for PCAN hardware.
    """
    try:
        bus = can.interface.Bus(channel=channel, bustype='pcan', bitrate=bitrate)
        print("PCAN bus initialized successfully.")
        return bus
    except Exception as e:
        print(f"Error initializing PCAN bus: {e}")
        return None

def send_single_can_message(bus, message_id, data):
    """
    Send a single CAN message.
    """
    try:
        message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
        bus.send(message)
        print(f"Sent message: ID={hex(message_id)}, Data={data}")
    except Exception as e:
        print(f"Error sending CAN message: {e}")

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"  # Replace with your actual PCAN channel
    BITRATE = 500000          # CAN bitrate
    MESSAGE_ID = 0x00000008
    DATA = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)
    
    if bus:
        # Send the single message
        send_single_can_message(bus, MESSAGE_ID, DATA)
        
        # Close the bus connection
        bus.shutdown()