import can
import re

def initialize_bus(channel="PCAN_USBBUS1", bitrate=500000):
    """Initialize the CAN bus using python-can for PCAN hardware."""
    try:
        bus = can.interface.Bus(channel=channel, bustype='pcan', bitrate=bitrate)
        print("PCAN bus initialized successfully.")
        return bus
    except Exception as e:
        print(f"Error initializing PCAN bus: {e}")
        return None

def parse_trc_file(filename):
    """Parse a .trc file and extract CAN messages."""
    can_messages = []
    
    with open(filename, "r") as file:
        for line in file:
            # Use regex to extract the relevant parts (timestamp, ID, DLC, data bytes)
            match = re.match(r"\s*\d+\)\s+([\d\.]+)\s+Rx\s+([\dA-Fa-f]+)\s+(\d+)\s+((?:[\dA-Fa-f]{2} )+)", line)
            if match:
                timestamp = float(match.group(1))  # Extract timestamp
                message_id = int(match.group(2), 16)  # Convert HEX string to integer
                dlc = int(match.group(3))  # Data Length Code (DLC)
                data = [int(byte, 16) for byte in match.group(4).strip().split()]  # Convert HEX bytes to integers
                
                can_messages.append((timestamp, message_id, data))
    
    return can_messages

def send_can_messages(bus, messages):
    """Send CAN messages through PCAN."""
    try:
        for timestamp, message_id, data in messages:
            message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
            bus.send(message)
            print(f"Sent message: ID={hex(message_id)}, Data={data}")
    except Exception as e:
        print(f"Error sending CAN messages: {e}")

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"
    BITRATE = 500000
    TRC_FILE = r"C:\Users\kamalesh.kb\Trace\trc_Battery_cutoff.trc"  # Replace with your actual .trc file

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)

    if bus:
        # Parse the .trc file
        can_messages = parse_trc_file(TRC_FILE)

        if can_messages:
            # Send the parsed CAN messages
            send_can_messages(bus, can_messages)
        
        # Close the bus connection
        bus.shutdown()
