import os
from gtts import gTTS

# Input text
text = "I was a bit happy with the last mission impossible movie as it was average but not too good!"

# Convert text to speech
tts = gTTS(text)

# Specify the folder where the file will be saved
folder_path = r"D:\second_life\Youtube_audio_pythonCreated"  # Replace this with your desired folder location
file_name = "output.mp3"

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Save the audio file in the specified folder
file_path = os.path.join(folder_path, file_name)
tts.save(file_path)

print(f"Audio saved at: {file_path}")
