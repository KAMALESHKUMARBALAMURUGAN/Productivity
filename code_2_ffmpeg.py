import os
from PIL import Image

image_path = r"E:\Automating_youtube_short_creation\assets\background.jpg"  # Your background image
audio_path = r"E:\Automating_youtube_short_creation\code\Productivity.mp3"   # Your TTS audio
output_path = r"E:\Automating_youtube_short_creation\output\short_video.mp4"

img = Image.open(image_path)
# Resize to even dimensions (e.g., 1280x720)
img = img.resize((1280, 720))
img.save(image_path)
# Duration can be automatically detected from audio
cmd = f'ffmpeg -loop 1 -i "{image_path}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest -y "{output_path}"'

os.system(cmd)

print("🎬 Video created successfully!")
