import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
from tkinter import Tk, Label, Entry, Button, Text, filedialog, messagebox, StringVar

# Function to convert text to images and then to video
def create_video():
    # Get the text from the Text box
    text = text_box.get("1.0", "end").strip()
    
    # Get the filename from the entry
    file_name = file_name_entry.get()

    # Check if user has entered both text and file name
    if not text or not file_name:
        messagebox.showerror("Error", "Please enter both text and filename!")
        return

    # Get the folder path
    folder_path = folder_path_var.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder!")
        return

    # Create the full file path
    file_path = os.path.join(folder_path, file_name + ".mp4")

    # Create frames (images) from the text
    frames = []
    font = ImageFont.load_default()
    
    # Split text into chunks to simulate multiple frames (1 sentence per frame)
    lines = text.split('.')
    
    for i, line in enumerate(lines):
        # Create an image with the text
        img = Image.new('RGB', (1280, 720), color=(0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((50, 300), line.strip(), font=font, fill=(255, 255, 255))
        
        # Save each frame as an image
        frame_path = os.path.join(folder_path, f"frame_{i}.png")
        img.save(frame_path)
        frames.append(frame_path)

    # Create a video from the frames using MoviePy
    clip = ImageSequenceClip(frames, fps=1)  # 1 frame per second

    # Save the video
    clip.write_videofile(file_path, fps=1)

    # Cleanup frames
    for frame in frames:
        os.remove(frame)

    messagebox.showinfo("Success", f"Video saved at: {file_path}")

# Initialize the Tkinter window
root = Tk()
root.title("Text to Video Converter")
root.geometry("500x500")

# Label and Text box for input text
Label(root, text="Enter the text:").pack(pady=10)
text_box = Text(root, height=5, width=40)
text_box.pack(pady=10)

# Label and Entry for filename
Label(root, text="Enter the filename (without extension):").pack(pady=5)
file_name_entry = Entry(root, width=30)
file_name_entry.pack(pady=5)

# Label and Entry for folder path (user-selected)
Label(root, text="Selected Folder:").pack(pady=5)
folder_path_var = StringVar()  # To store the folder path
folder_path_entry = Entry(root, textvariable=folder_path_var, width=40, state="readonly")
folder_path_entry.pack(pady=5)

# Button to browse and select folder
def browse_folder():
    folder_path = filedialog.askdirectory(title="Select folder to save the file")
    if folder_path:
        folder_path_var.set(folder_path)

Button(root, text="Browse Folder", command=browse_folder).pack(pady=5)

# Button to create video
Button(root, text="Create Video", command=create_video).pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
