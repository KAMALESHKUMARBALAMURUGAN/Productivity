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

def speed_to_rpm(speed):
    """Convert speed (in km/h) to RPM."""
    return int(speed / 0.092)

def rpm_to_bytes(rpm):
    """Convert RPM to two bytes in reverse order."""
    hex_rpm = f"{rpm:04X}"  # Convert to 4-digit hexadecimal
    byte1 = int(hex_rpm[2:], 16)  # Lower byte
    byte0 = int(hex_rpm[:2], 16)  # Higher byte
    return [byte1, byte0]

def generate_speed_messages(start_speed, end_speed, interval):
    """Generate CAN messages for speeds within a given range and interval."""
    messages = []
    for speed in range(start_speed, end_speed + 1, interval):
        rpm = speed_to_rpm(speed)
        byte_data = rpm_to_bytes(rpm)
        # Construct the full message data
        data = [byte_data[0], byte_data[1], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        messages.append(data)
        print(f"Speed: {speed} kmph -> RPM: {rpm} -> Data: {data}")
    return messages

def send_speed_messages(bus, message_id, interval_ms, speed_messages):
    """Send the generated speed messages over the CAN bus."""
    try:
        for data in speed_messages:
            # Create a CAN message
            message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
            # Send the message
            bus.send(message)
            print(f"Sent message: ID={hex(message_id)}, Data={data}")
            # Wait for the specified interval
            time.sleep(interval_ms / 1500.0)
    except Exception as e:
        print(f"Error sending speed messages: {e}")

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"  # Replace with your actual PCAN channel
    BITRATE = 500000          # CAN bitrate
    MESSAGE_ID = 0x14520902   # Example CAN message ID
    START_SPEED = 0           # Start speed in km/h
    END_SPEED = 68            # End speed in km/h
    INTERVAL_SPEED = 4        # Speed interval in km/h
    INTERVAL_MS = 700        # Message interval in milliseconds

    # Generate speed messages
    speed_messages = generate_speed_messages(START_SPEED, END_SPEED, INTERVAL_SPEED)

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)

    if bus:
        # Send speed messages
        send_speed_messages(bus, MESSAGE_ID, INTERVAL_MS, speed_messages)
        # Close the bus connection
        bus.shutdown()
