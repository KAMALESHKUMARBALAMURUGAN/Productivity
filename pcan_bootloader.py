import can
import re
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

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
            timestamp = float(parts[1])
            message_id = int(parts[3], 16)
            dlc = int(parts[4])
            data = [int(byte, 16) for byte in parts[5:5+dlc]]
            can_messages.append((timestamp, message_id, data))

    return can_messages

def send_can_messages(bus, messages):
    """Send CAN messages through PCAN."""
    ignored_ids = {0x108, 0x112, 0x111, 0x113, 0x110, 0x10f, 0x109, 0x114}
    try:
        start_time = time.time()
        last_sent_times = {}
        for timestamp, message_id, data in messages:
            if message_id in ignored_ids:
                print(f"Ignoring message with ID={hex(message_id)}")
                continue
            if message_id in last_sent_times:
                time_offset = timestamp - last_sent_times[message_id]
            else:
                time_offset = timestamp - (time.time() - start_time)
            
            time_offset = time_offset / 1000
            time.sleep(time_offset)
            
            message = can.Message(arbitration_id=message_id, data=data, is_extended_id=True)
            bus.send(message)
            last_sent_times[message_id] = timestamp
    except Exception as e:
        print(f"Error sending CAN messages: {e}")

def check_mcu_available(bus):
    """Check if the MCU is available by reading a specific CAN message."""
    try:
        message = bus.recv(timeout=1)
        if message and message.arbitration_id == 0x108:
            return True
        return False
    except Exception as e:
        print(f"Error checking MCU availability: {e}")
        return False

def select_binary_file():
    """Open a file dialog to select the binary file."""
    file_path = filedialog.askopenfilename(filetypes=[("Trace Files", "*.trc")])
    return file_path

def start_flashing(bus, trc_file):
    """Start the flashing process."""
    can_messages = parse_trc_file(trc_file)
    if can_messages:
        send_can_messages(bus, can_messages)
        messagebox.showinfo("Success", "Flashing process completed successfully.")
    else:
        messagebox.showerror("Error", "No CAN messages found in the selected file.")

def create_ui():
    """Create the Tkinter UI."""
    root = tk.Tk()
    root.title("PCAN Bootloader")

    # Display Lectrix logo
    logo = Image.open(r"C:\Users\kamalesh.kb\KAMALESH_PRODUCTIVITY\Productivity\LECTRIX_LOGO.jpg")  # Replace with your actual logo file
    logo = logo.resize((600, 200), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(root, image=logo_img)
    logo_label.pack(pady=10)

    # Check MCU availability
    bus = initialize_bus()
    if bus and check_mcu_available(bus):
        mcu_status = tk.Label(root, text="MCU Available", fg="green")
    else:
        mcu_status = tk.Label(root, text="MCU Not Available", fg="red")
    mcu_status.pack(pady=10)

    # Select binary file
    select_file_button = tk.Button(root, text="Select Binary File", command=lambda: select_binary_file())
    select_file_button.pack(pady=10)

    # Start flashing process
    start_button = tk.Button(root, text="Start Flashing", command=lambda: start_flashing(bus, select_binary_file()))
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_ui()