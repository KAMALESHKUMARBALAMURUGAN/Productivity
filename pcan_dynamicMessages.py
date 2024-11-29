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

def send_can_messages(bus, messages, always_present_message=None):
    """
    Send a series of CAN messages with specified data and intervals.
    """
    try:
        while True:
            for message_id, interval_ms, data_list in messages:
                for data in data_list:
                    # Create a CAN message
                    message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
                    # Send the message
                    bus.send(message)
                    print(f"Sent message: ID={hex(message_id)}, Data={data}")
                    # Wait for the specified interval
                    time.sleep(interval_ms / 1000.0)
            
            # Send the always-present message if provided
            if always_present_message:
                always_message_id, always_interval_ms, always_data_list = always_present_message
                for data in always_data_list:
                    message = can.Message(arbitration_id=always_message_id, data=data, is_extended_id=True)
                    bus.send(message)
                    print(f"Sent always-present message: ID={hex(always_message_id)}, Data={data}")
                    time.sleep(always_interval_ms / 1000.0)
    except Exception as e:
        print(f"Error sending CAN messages: {e}")

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"  # Replace with your actual PCAN channel
    BITRATE = 500000          # CAN bitrate

    # Ensure this message is always included
    ALWAYS_PRESENT_MESSAGE = (0x18530902, 1000, [
        [0x00, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    ])

    # Messages configuration
    MESSAGES = [
        (0x00000008, 250, [
            [num, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] for num in range(0x01, 0x65)
        ]),
        (0x00000006, 100, [
            [0x00, 0x00, 0x00, 0x00],
            [0xFF, 0xFF, 0xE4, 0xA8],
            [0xFF, 0xFF, 0xE0, 0xC0],
            [0xFF, 0xFF, 0xD1, 0x20],
            [0xFF, 0xFF, 0xC9, 0x50],
            [0xFF, 0xFF, 0xBD, 0x10],
            [0xFF, 0xFF, 0xB5, 0x40],
            [0xFF, 0xFF, 0xAD, 0x70],
            [0xFF, 0xFF, 0xA5, 0xA0],
            [0xFF, 0xFF, 0x9D, 0xD0],
            [0xFF, 0xFF, 0x92, 0xC0],
            [0xFF, 0xFF, 0x8A, 0xF0],
            [0xFF, 0xFF, 0x83, 0x20],
            [0xFF, 0xFF, 0x7B, 0x50],
            [0xFF, 0xFF, 0x77, 0x68],
            [0xFF, 0xFF, 0x15, 0xA0],
            [0xFF, 0xFF, 0x77, 0x68],
            [0xFF, 0xFF, 0x7B, 0x50],
            [0xFF, 0xFF, 0x83, 0x20],
            [0xFF, 0xFF, 0x8A, 0xF0],
            [0xFF, 0xFF, 0x92, 0xC0],
            [0xFF, 0xFF, 0x9D, 0xD0],
            [0xFF, 0xFF, 0xA5, 0xA0],
            [0xFF, 0xFF, 0xAD, 0x70],
            [0xFF, 0xFF, 0xB5, 0x40],
            [0xFF, 0xFF, 0xBD, 0x10],
            [0xFF, 0xFF, 0xC9, 0x50],
            [0xFF, 0xFF, 0xD1, 0x20],
            [0xFF, 0xFF, 0xE0, 0xC0],
            [0xFF, 0xFF, 0xE4, 0xA8]
        ]),   
    ]

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)

    if bus:
        # Check if ALWAYS_PRESENT_MESSAGE is in MESSAGES
        if ALWAYS_PRESENT_MESSAGE not in MESSAGES:
            # Send messages with ALWAYS_PRESENT_MESSAGE
            send_can_messages(bus, MESSAGES, ALWAYS_PRESENT_MESSAGE)
        else:
            # Send messages without ALWAYS_PRESENT_MESSAGE
            send_can_messages(bus, MESSAGES)
        # Close the bus connection
        bus.shutdown()