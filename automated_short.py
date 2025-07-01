import os
from PIL import Image
from gtts import gTTS

# Step 1: Text-to-Speech
quote = "Don't lie on the couch and wait for inspiration to come. Get up and get to work. Consistency wins. Keep showing up."
tts = gTTS(text=quote, lang='en')

audio_path = r"E:\Automating_youtube_short_creation\audio\audio.mp3"
tts.save(audio_path)
print(f"🎧 Audio saved at: {audio_path}")

# Step 2: Define image paths & durations
images_with_duration = [
    (r"E:\Automating_youtube_short_creation\assets\img1.jpg", 2),
    (r"E:\Automating_youtube_short_creation\assets\img2.jpg", 2),
    (r"E:\Automating_youtube_short_creation\assets\img3.jpg", 4)
]

ffmpeg_input_txt = r"E:\Automating_youtube_short_creation\assets\ffmpeg_input.txt"

# Step 3: Resize images to 1280x720 and prepare ffmpeg input
with open(ffmpeg_input_txt, 'w') as f:
    for img_path, duration in images_with_duration:
        img = Image.open(img_path)
        img = img.resize((1280, 720))
        img.save(img_path)  # overwrite with resized version

        f.write(f"file '{img_path}'\n")
        f.write(f"duration {duration}\n")

    # Repeat last frame to avoid FFmpeg freeze
    f.write(f"file '{images_with_duration[-1][0]}'\n")

# Step 4: Generate temp video from images
temp_video_path = r"E:\Automating_youtube_short_creation\output\temp_video.mp4"
cmd1 = f'ffmpeg -y -f concat -safe 0 -i "{ffmpeg_input_txt}" -vsync vfr -pix_fmt yuv420p "{temp_video_path}"'
os.system(cmd1)
print("📸 Image slideshow video created.")

# Step 5: Combine with audio
final_video_path = r"E:\Automating_youtube_short_creation\output\short_video.mp4"
cmd2 = f'ffmpeg -y -i "{temp_video_path}" -i "{audio_path}" -c:v copy -c:a aac -shortest "{final_video_path}"'
os.system(cmd2)

print("🎬 Final video with audio created successfully!")
