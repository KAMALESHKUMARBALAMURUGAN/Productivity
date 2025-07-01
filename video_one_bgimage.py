import os
from PIL import Image
from gtts import gTTS

quote = "Don't lie on the couch and wait for inspiration to come. Get up and get to work. Consistency wins. Keep showing up."
tts = gTTS(text=quote, lang='en')

# Save to a custom location
audio_path = r"E:\Automating_youtube_short_creation\audio\audio.mp3"
tts.save(audio_path)

print(f"Audio saved at: {audio_path}")


image_path = r"E:\Automating_youtube_short_creation\assets\background.jpg"  # Your background image
output_path = r"E:\Automating_youtube_short_creation\output\short_video.mp4"

img = Image.open(image_path)
# Resize to even dimensions (e.g., 1280x720)
img = img.resize((1280, 720))
img.save(image_path)
# Duration can be automatically detected from audio
cmd = f'ffmpeg -loop 1 -i "{image_path}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest -y "{output_path}"'

os.system(cmd)

print("🎬 Video created successfully!")
