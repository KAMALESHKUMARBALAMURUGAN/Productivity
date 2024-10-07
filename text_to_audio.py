import os
from tkinter import Tk, Label, Entry, Button, Text, filedialog, messagebox
from gtts import gTTS

# Function to save the text as speech
def save_as_audio():
    # Get the text from the Text box
    text = text_box.get("1.0", "end").strip()
    
    # Get the filename from the entry
    file_name = file_name_entry.get()
    
    # Check if user has entered both text and file name
    if not text or not file_name:
        messagebox.showerror("Error", "Please enter both text and filename!")
        return
    
    # Get the folder path where user wants to save the file
    folder_path = filedialog.askdirectory(title="Select folder to save the file")
    if not folder_path:  # If user doesn't select a folder
        messagebox.showerror("Error", "Please select a folder!")
        return
    
    # Create the full file path
    file_path = os.path.join(folder_path, file_name + ".mp3")
    
    # Convert text to speech and save it
    tts = gTTS(text)
    tts.save(file_path)
    
    messagebox.showinfo("Success", f"Audio saved at: {file_path}")

# Initialize the Tkinter window
root = Tk()
root.title("Text to Speech Converter")
root.geometry("400x300")

# Label and Text box for input text
Label(root, text="Enter the text:").pack(pady=10)
text_box = Text(root, height=5, width=40)
text_box.pack(pady=10)

# Label and Entry for filename
Label(root, text="Enter the filename (without extension):").pack(pady=5)
file_name_entry = Entry(root, width=30)
file_name_entry.pack(pady=5)

# Save button to trigger the save_as_audio function
Button(root, text="Convert and Save", command=save_as_audio).pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
