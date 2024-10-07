import os
from tkinter import Tk, Label, Entry, Button, Text, filedialog, messagebox, StringVar, ttk
from gtts import gTTS

# Function to enable or disable the Submit button based on folder selection
def update_submit_button():
    if folder_path_var.get():  # If folder path is not empty
        submit_button.config(state="normal")
    else:
        submit_button.config(state="disabled")

# Function to browse and select folder
def browse_folder():
    folder_path = filedialog.askdirectory(title="Select folder to save the file")
    if folder_path:  # If a folder is selected
        folder_path_var.set(folder_path)
        update_submit_button()  # Enable the Submit button
    else:
        messagebox.showerror("Error", "Please Choose the folder before clicking the submit button!")

# Function to save the text as speech
def save_as_audio():
    # Get the text from the Text box
    text = text_box.get("1.0", "end").strip()
    
    # Get the filename from the entry
    file_name = file_name_entry.get()
    
    # Get the selected voice/accent from the ComboBox
    selected_voice = voice_var.get()
    
    # Check if user has entered both text and file name
    if not text or not file_name:
        messagebox.showerror("Error", "Please enter both text and filename!")
        return
    
    # Get the folder path from the variable
    folder_path = folder_path_var.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder!")
        return
    
    # Create the full file path
    file_path = os.path.join(folder_path, file_name + ".mp3")
    
    # Convert text to speech and save it based on selected voice/accent
    tts = gTTS(text, lang=selected_voice)
    tts.save(file_path)
    
    messagebox.showinfo("Success", f"Audio saved at: {file_path}")

# Initialize the Tkinter window
root = Tk()
root.title("Text to Speech Converter")
root.geometry("500x500")

# Label and Text box for input text
Label(root, text="Enter the text:").pack(pady=10)
text_box = Text(root, height=5, width=40)
text_box.pack(pady=10)

# Label and Entry for filename
Label(root, text="Enter the filename (without extension):").pack(pady=5)
file_name_entry = Entry(root, width=30)
file_name_entry.pack(pady=5)

# Label and ComboBox for selecting voice/accent
Label(root, text="Choose Voice/Accent:").pack(pady=5)
voice_var = StringVar()
voice_combobox = ttk.Combobox(root, textvariable=voice_var, state="readonly", width=25)
voice_combobox['values'] = ('en', 'en-uk', 'en-au', 'en-us')  # Different language accents for demo
voice_combobox.current(0)  # Set default to 'en'
voice_combobox.pack(pady=5)

# Label and Entry for folder path (user-selected)
Label(root, text="Selected Folder:").pack(pady=5)
folder_path_var = StringVar()  # To store the folder path
folder_path_entry = Entry(root, textvariable=folder_path_var, width=40, state="readonly")
folder_path_entry.pack(pady=5)

# Button to browse and select folder
Button(root, text="Browse Folder", command=browse_folder).pack(pady=5)

# Save button to trigger the save_as_audio function
submit_button = Button(root, text="Save", command=save_as_audio, state="disabled")
submit_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
