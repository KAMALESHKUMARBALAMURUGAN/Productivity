from gtts import gTTS

quote = "Consistency wins. Keep showing up."
tts = gTTS(text=quote, lang='en')

# Save to a custom location
save_path = r"E:\Automating_youtube_short_creation\code\Productivity.mp3"
tts.save(save_path)

print(f"Audio saved at: {save_path}")
