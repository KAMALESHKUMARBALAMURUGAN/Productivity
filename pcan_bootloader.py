import can
import re
import time

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
    cleaned_lines = []

    with open(filename, "r") as file:
        lines = file.readlines()
        cleaned_lines = lines[14:]  # Skip the first 14 lines

    with open("Cleaned_trc.trc", "w") as cleaned_file:
        cleaned_file.writelines(cleaned_lines)

    for line in cleaned_lines:
        parts = line.split()
        if len(parts) >= 6:
            print("parts[1]", parts[1])
            print("parts[3]", parts[3])
            print("parts[4]", parts[4])
            timestamp = float(parts[1])
            message_id = int(parts[3], 16)
            dlc = int(parts[4])
            data = [int(byte, 16) for byte in parts[5:5+dlc]]
            print("data", data)
            can_messages.append((timestamp, message_id, data))

    return can_messages

def send_can_messages(bus, messages):
    print("messages", messages)
    """Send CAN messages through PCAN."""
    try:
        start_time = time.time()
        last_sent_times = {}
        print("start_time", start_time)
        print("Last_sent_times", last_sent_times)
        for timestamp, message_id, data in messages:
            if message_id in last_sent_times:
                print("Not a new id")
                time_offset = timestamp - last_sent_times[message_id]
            else:
                print("New id")
                time_offset = timestamp - (time.time() - start_time)
            
            time_offset = time_offset / 1000
            print("time_offset", time_offset)
            time.sleep(time_offset)
            
            message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
            bus.send(message)
            print(f"Sent message: ID={hex(message_id)}, Data={data}")
            
            last_sent_times[message_id] = timestamp
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