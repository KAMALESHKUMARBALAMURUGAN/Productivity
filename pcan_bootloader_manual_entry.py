import can
import time

# List of IDs to check for
ids_to_check = [0x11A, 0x11B, 0x11C]
ids_to_check_2= [0x115]

# Map of FROM DEVICE messages to corresponding MCU messages
messages_to_send = [
    (0x00000110, [0x31, 0x32, 0x30, 0x30, 0x42, 0x30, 0x48, 0x54]),
    (0x0000010F, [0x41, 0x32, 0x33, 0x31, 0x51, 0x41, 0x30, 0x30]),
    (0x00000109, [0x44, 0x44, 0x37, 0x30, 0x30, 0x43, 0x20, 0x20]),
]

messages_to_send2 =[
    (0X00000114,[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
]
# Function to send a CAN message
def send_message(bus, id, data):
    msg = can.Message(arbitration_id=id, data=bytearray(data), is_extended_id=True)
    bus.send(msg)

# Function to read CAN messages

# Function to read CAN messages
def read_messages(bus):
    count = 0
    print("Listening for messages...")
    messages_sent = False
    messages_sent2 = False
    while True:
        msg = bus.recv()
        if msg.arbitration_id in ids_to_check and not messages_sent:
            print("Received message from device: " + hex(msg.arbitration_id))
            for mcu_id, mcu_data in messages_to_send:
                send_message(bus, mcu_id, mcu_data)
                print("Sent message to MCU: " + hex(mcu_id) + " with data: " + str(mcu_data))
            messages_sent = True
        elif msg.arbitration_id in ids_to_check_2 and not messages_sent2:
            print("Received message from device: " + hex(msg.arbitration_id))
            for mcu_id, mcu_data in messages_to_send2:
                count += 1
                send_message(bus, mcu_id, mcu_data)
                print("Sent message to MCU: " + hex(mcu_id) + " with data: " + str(mcu_data))
            # messages_sent2 = True
        print("count----->",count)
        # time.sleep(0.1)
    

# Initialize CAN bus
bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)

try:
    read_messages(bus)
except KeyboardInterrupt:
    pass
finally:
    bus.shutdown()