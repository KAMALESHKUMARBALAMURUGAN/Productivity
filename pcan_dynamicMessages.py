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

def send_can_messages(bus, message_id, interval_ms, data_list):
    """
    Send a series of CAN messages with specified data and intervals.
    """
    try:
        for data in data_list:
            # Create a CAN message
            message = can.Message(arbitration_id=message_id, data=data, is_extended_id=False)
            # Send the message
            bus.send(message)
            print(f"Sent message: ID={hex(message_id)}, Data={data}")
            # Wait for the specified interval
            time.sleep(interval_ms / 1000.0)
    except Exception as e:
        print(f"Error sending CAN messages: {e}")

if __name__ == "__main__":
    # Configuration
    CHANNEL = "PCAN_USBBUS1"  # Replace with your actual PCAN channel
    BITRATE = 500000          # CAN bitrate
    MESSAGE_ID = 0x00000006       # Example CAN message ID
    INTERVAL_MS = 100    # Interval in milliseconds
    DATA_LIST = [            # Example data payloads
        # [0x00, 0x00, 0x3d, 0x00,0x00, 0x00, 0x00, 0x00],  # 0000
        # [0x00, 0x00, 0x3c, 0x00,0x00, 0x00, 0x00, 0x00],  # 0000
        # [0x00, 0x00, 0x3b, 0x00,0x00, 0x00, 0x00, 0x00],  # 0000
        # [0x00, 0x00, 0x3a, 0x00,0x00, 0x00, 0x00, 0x00],  # 0000
        # [0x00, 0x00, 0x39, 0x00,0x00, 0x00, 0x00, 0x00],  # 0000
        # [0x00, 0x00, 0x38, 0x00,0x00, 0x00, 0x00, 0x00],  # 0000
        

        

        # #toggling all segments one by one
        [0x00, 0x00, 0x00, 0x00],  # 0000
        [0xFF, 0xFF, 0xE4, 0xA8],  # -7000
        [0xFF, 0xFF, 0xE0, 0xC0],  # -8000
        [0xFF, 0xFF, 0xD1, 0x20],  # -12000
        [0xFF, 0xFF, 0xC9, 0x50],  # -14000
        [0xFF, 0xFF, 0xBD, 0x10],  # -17000
        [0xFF, 0xFF, 0xB5, 0x40],  # -19000
        [0xFF, 0xFF, 0xAD, 0x70],  # -21000
        [0xFF, 0xFF, 0xA5, 0xA0],  # -23000
        [0xFF, 0xFF, 0x9D, 0xD0],  # -25000
        [0xFF, 0xFF, 0x92, 0xC0],  # -28000
        [0xFF, 0xFF, 0x8A, 0xF0],  # -30000
        [0xFF, 0xFF, 0x83, 0x20],  # -32000
        [0xFF, 0xFF, 0x7B, 0x50],  # -34000
        [0xFF, 0xFF, 0x77, 0x68],  # -35000
        [0xFF, 0xFF, 0x15, 0xA0],  # -60000

        
        
        [0xFF, 0xFF, 0x77, 0x68],  # -35000
        [0xFF, 0xFF, 0x7B, 0x50],  # -34000
        [0xFF, 0xFF, 0x83, 0x20],  # -32000
        [0xFF, 0xFF, 0x8A, 0xF0],  # -30000
        [0xFF, 0xFF, 0x92, 0xC0],  # -28000
        [0xFF, 0xFF, 0x9D, 0xD0],  # -25000
        [0xFF, 0xFF, 0xA5, 0xA0],  # -23000
        [0xFF, 0xFF, 0xAD, 0x70],  # -21000
        [0xFF, 0xFF, 0xB5, 0x40],  # -19000
        [0xFF, 0xFF, 0xBD, 0x10],  # -17000
        [0xFF, 0xFF, 0xC9, 0x50],  # -14000
        [0xFF, 0xFF, 0xD1, 0x20],  # -12000
        [0xFF, 0xFF, 0xE0, 0xC0],  # -8000
        [0xFF, 0xFF, 0xE4, 0xA8]   # -7000
    


        # 15 MESSAGES WITH 3 SETS OF DATA WHICH CAN TURN ON DIFFERENT NO OF SEGMENTS
        # [0x00, 0x00, 0x00, 0x00],  # `ffffb5b6` split into bytes - 0000
        # [0xFF, 0xFF, 0x9E, 0x46],  # `ffff86d6` split into bytes - -25018
        # [0xFF, 0xFF, 0x77, 0x36],  # `ffff3c4e` split into bytes - -35018
        
        # [0x00, 0x00, 0x00, 0x00],  
        # [0xFF, 0xFF, 0x9E, 0x46],  
        # [0xFF, 0xFF, 0x77, 0x36],  # `ffff3c4e` split into bytes - -35018
        
        # [0x00, 0x00, 0x00, 0x00],  # `ffffb5b6` split into bytes - 0000
        # [0xFF, 0xFF, 0x9E, 0x46],  # `ffff86d6` split into bytes - -25018
        # [0xFF, 0xFF, 0x77, 0x36],  # `ffff3c4e` split into bytes - -35018

        # [0x00, 0x00, 0x00, 0x00],  # `ffffb5b6` split into bytes - 0000
        # [0xFF, 0xFF, 0x9E, 0x46],  # `ffff86d6` split into bytes - -25018
        # [0xFF, 0xFF, 0x77, 0x36],  # `ffff3c4e` split into bytes - -35018

        # [0x00, 0x00, 0x00, 0x00],  # `ffffb5b6` split into bytes - 0000
        # [0xFF, 0xFF, 0x9E, 0x46],  # `ffff86d6` split into bytes - -25018
        # [0xFF, 0xFF, 0x77, 0x36],  # `ffff3c4e` split into bytes - -35018
        

        #POSITIVE AND NEGATIVE VALUES
            # [0xFF, 0xFF, 0x77, 0x36],  # `ffff86d6` split into bytes = -35018
            # [0X00, 0X00, 0X88, 0XCA],  # `ffffb5b6` split into bytes = 35018

            
            # [0xFF, 0xFF, 0x77, 0x36],  # `ffff86d6` split into bytes = -35018
            # [0X00, 0X00, 0X61, 0XBA],  # `ffffb5b6` split into bytes = 35018

            # [0xFF, 0xFF, 0x77, 0x36],  # `ffff86d6` split into bytes = -35018
            # [0X00, 0X00, 0X61, 0XBA],  # `ffffb5b6` split into bytes = 35018

            # [0xFF, 0xFF, 0x77, 0x36],  # `ffff86d6` split into bytes = -35018
            # [0X00, 0X00, 0X61, 0XBA],  # `ffffb5b6` split into bytes = 35018
            
            # [0xFF, 0xFF, 0x77, 0x36],  # `ffff86d6` split into bytes = -35018
            # [0X00, 0X00, 0X61, 0XBA],  # `ffffb5b6` split into bytes = 35018

            # [0xFF, 0xFF, 0x77, 0x36],  # `ffff86d6` split into bytes = -35018
            # [0X00, 0X00, 0X61, 0XBA],  # `ffffb5b6` split into bytes = 35018

        #all segments


    ]
    
    

    # Initialize the bus
    bus = initialize_bus(CHANNEL, BITRATE)

    if bus:
        # Send messages
        send_can_messages(bus, MESSAGE_ID, INTERVAL_MS, DATA_LIST)
        # Close the bus connection
        bus.shutdown()
